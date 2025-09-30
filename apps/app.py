import io
import json
import re
import time
import zipfile
import hashlib
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import pandas as pd
import streamlit as st

# ---- Label Studio SDK: handle both "Client" and older "LabelStudio" naming ----
ClientType = None
try:
    from label_studio_sdk import Client as _Client
    ClientType = _Client
except Exception:
    try:
        from label_studio_sdk import LabelStudio as _Client
        ClientType = _Client
    except Exception:
        ClientType = None

# =========================
# SDK helpers
# =========================
@st.cache_data(show_spinner=False)
def connect_ls(base_url: str, api_key: str):
    if ClientType is None:
        raise RuntimeError(
            "label-studio-sdk not found or incompatible. Please `pip install label-studio-sdk`."
        )
    try:
        client = ClientType(url=base_url, api_key=api_key)  # modern
    except TypeError:
        client = ClientType(base_url=base_url, api_key=api_key)  # legacy
    return client


def _obj_to_dict(x: Any) -> Dict[str, Any]:
    if x is None:
        return {}
    if isinstance(x, dict):
        return x
    for key in ("to_dict", "dict"):
        if hasattr(x, key) and callable(getattr(x, key)):
            try:
                return getattr(x, key)()
            except Exception:
                pass
    try:
        return {k: getattr(x, k) for k in dir(x) if not k.startswith("_")}
    except Exception:
        return {"value": str(x)}


def _safe_attr(x: Any, name: str, default=None):
    try:
        return getattr(x, name)
    except Exception:
        try:
            d = _obj_to_dict(x)
            return d.get(name, default)
        except Exception:
            return default


def list_projects(client) -> List[Any]:
    try:
        # Try modern SDK first
        if hasattr(client, 'projects') and hasattr(client.projects, 'list'):
            return list(client.projects.list(page_size=1000))
        elif hasattr(client, 'list_projects'):
            return list(client.list_projects())
        elif hasattr(client, 'get_projects'):
            return list(client.get_projects())
        else:
            # Fallback to direct API call
            import requests
            # Try Bearer token first (LS 1.20+), then Token (legacy)
            for auth_type in ["Bearer", "Token"]:
                response = requests.get(f"{client.url}/api/projects/", headers={"Authorization": f"{auth_type} {client.api_key}"})
                if response.status_code != 401:
                    response.raise_for_status()
                    return response.json()
            # If both fail, raise the last error
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise RuntimeError(f"Could not list projects: {e}")


def get_project(client, pid: int):
    try:
        # Try modern SDK first
        if hasattr(client, 'projects') and hasattr(client.projects, 'get'):
            return client.projects.get(id=pid)
        elif hasattr(client, 'get_project'):
            return client.get_project(pid)
        else:
            # Fallback to direct API call
            import requests
            # Try Bearer token first (LS 1.20+), then Token (legacy)
            for auth_type in ["Bearer", "Token"]:
                response = requests.get(f"{client.url}/api/projects/{pid}/", headers={"Authorization": f"{auth_type} {client.api_key}"})
                if response.status_code != 401:
                    response.raise_for_status()
                    return response.json()
            # If both fail, raise the last error
            response.raise_for_status()
            return response.json()
    except Exception:
        # Fallback: search in projects list
        projs = list_projects(client)
        for p in projs:
            if int(_safe_attr(p, "id")) == int(pid):
                return p
        raise RuntimeError(f"Project {pid} not found")


def label_config_of(project) -> str:
    return _safe_attr(project, "label_config", "")


# =========================
# Exporters (stream + snapshot)
# =========================

def tasks_iter(client, project_id: int, fields: str = "all", page_size: int = 1000):
    try:
        # Try modern SDK first
        if hasattr(client, 'tasks') and hasattr(client.tasks, 'list'):
            for t in client.tasks.list(project=project_id, fields=fields, page_size=page_size):
                yield t
        elif hasattr(client, 'get_project_tasks'):
            tasks = client.get_project_tasks(project_id)
            for t in tasks:
                yield t
        else:
            # Fallback to direct API call
            import requests
            page = 1
            # Try Bearer token first (LS 1.20+), then Token (legacy)
            auth_header = None
            for auth_type in ["Bearer", "Token"]:
                test_response = requests.get(
                    f"{client.url}/api/projects/{project_id}/tasks/",
                    headers={"Authorization": f"{auth_type} {client.api_key}"},
                    params={"page": 1, "page_size": 1}
                )
                if test_response.status_code != 401:
                    auth_header = {"Authorization": f"{auth_type} {client.api_key}"}
                    break
            
            if not auth_header:
                raise RuntimeError("Authentication failed with both Bearer and Token formats")
            
            while True:
                response = requests.get(
                    f"{client.url}/api/projects/{project_id}/tasks/",
                    headers=auth_header,
                    params={"page": page, "page_size": page_size}
                )
                response.raise_for_status()
                data = response.json()
                
                if isinstance(data, dict) and 'results' in data:
                    tasks = data['results']
                    if not tasks:
                        break
                    for t in tasks:
                        yield t
                    if not data.get('next'):
                        break
                    page += 1
                elif isinstance(data, list):
                    for t in data:
                        yield t
                    break
                else:
                    break
    except Exception as e:
        st.warning(f"Could not iterate tasks for project {project_id}: {e}")
        return


def build_export_stream(
    client,
    project_id: int,
    include_annotations: bool = True,
    include_predictions: bool = False,
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for t in tasks_iter(client, project_id, fields="all", page_size=1000):
        item: Dict[str, Any] = {"data": dict(_safe_attr(t, "data", {}) or {})}
        if include_annotations:
            anns = []
            for a in (_safe_attr(t, "annotations", []) or []):
                anns.append({"result": _safe_attr(a, "result", [])})
            if anns:
                item["annotations"] = anns
        if include_predictions:
            preds = []
            for p in (_safe_attr(t, "predictions", []) or []):
                preds.append({"result": _safe_attr(p, "result", [])})
            if preds:
                item["predictions"] = preds
        out.append(item)
    return out


def build_export_snapshot(client, project_id: int, poll_seconds: int = 2, timeout: int = 1800) -> List[Dict[str, Any]]:
    """Create a server-side export snapshot, download ZIP, and extract tasks JSON.
    Returns a list[task]. Assumes default LS export format.
    """
    # Create export
    try:
        # Try different SDK methods
        if hasattr(client, 'projects') and hasattr(client.projects, 'exports'):
            snap = client.projects.exports.create(id=project_id, title=f"snapshot-{project_id}")
        elif hasattr(client, 'make_request'):
            # Direct API call through SDK
            snap = client.make_request('POST', f'/api/projects/{project_id}/exports/', json={'title': f"snapshot-{project_id}"})
        else:
            # Fallback to requests
            import requests
            # Try Bearer token first (LS 1.20+), then Token (legacy)
            for auth_type in ["Bearer", "Token"]:
                response = requests.post(
                    f"{client.url}/api/projects/{project_id}/exports/",
                    headers={"Authorization": f"{auth_type} {client.api_key}"},
                    json={'title': f"snapshot-{project_id}"}
                )
                if response.status_code != 401:
                    response.raise_for_status()
                    snap = response.json()
                    break
            else:
                response.raise_for_status()
                snap = response.json()
    except Exception as e:
        # Fallback to stream export if snapshot fails
        st.warning(f"Snapshot export failed for project {project_id}, falling back to stream export: {e}")
        return build_export_stream(client, project_id, include_annotations=True, include_predictions=False)

    snap_id = _safe_attr(snap, "id")
    status = _safe_attr(snap, "status", "")

    # Poll
    start = time.time()
    while status not in ("completed", "failed", "error"):
        time.sleep(poll_seconds)
        # refresh snapshot status
        try:
            if hasattr(client, 'projects') and hasattr(client.projects, 'exports'):
                snap = client.projects.exports.get(id=project_id, export_id=snap_id)
            else:
                # Fallback API call
                import requests
                # Try Bearer token first (LS 1.20+), then Token (legacy)
                for auth_type in ["Bearer", "Token"]:
                    response = requests.get(
                        f"{client.url}/api/projects/{project_id}/exports/{snap_id}/",
                        headers={"Authorization": f"{auth_type} {client.api_key}"}
                    )
                    if response.status_code != 401:
                        response.raise_for_status()
                        snap = response.json()
                        break
                else:
                    response.raise_for_status()
                    snap = response.json()
            status = _safe_attr(snap, "status", "")
        except Exception:
            # Some SDKs don't expose .get(); try listing and filtering
            try:
                if hasattr(client, 'projects') and hasattr(client.projects, 'exports'):
                    exps = client.projects.exports.list(id=project_id)
                else:
                    import requests
                    # Try Bearer token first (LS 1.20+), then Token (legacy)
                    for auth_type in ["Bearer", "Token"]:
                        response = requests.get(
                            f"{client.url}/api/projects/{project_id}/exports/",
                            headers={"Authorization": f"{auth_type} {client.api_key}"}
                        )
                        if response.status_code != 401:
                            response.raise_for_status()
                            exps = response.json()
                            break
                    else:
                        response.raise_for_status()
                        exps = response.json()
                
                for e in exps:
                    if _safe_attr(e, "id") == snap_id:
                        status = _safe_attr(e, "status", "")
                        break
            except Exception:
                break
                
        if time.time() - start > timeout:
            raise TimeoutError(f"Snapshot export timed out for project {project_id}")

    if status != "completed":
        raise RuntimeError(f"Snapshot export ended with status '{status}' for project {project_id}")

    # Download ZIP into memory
    buf = io.BytesIO()
    try:
        if hasattr(client, 'projects') and hasattr(client.projects, 'exports'):
            client.projects.exports.download(id=project_id, export_id=snap_id, path=buf)
        else:
            # Fallback download
            import requests
            # Try Bearer token first (LS 1.20+), then Token (legacy)
            for auth_type in ["Bearer", "Token"]:
                response = requests.get(
                    f"{client.url}/api/projects/{project_id}/exports/{snap_id}/download/",
                    headers={"Authorization": f"{auth_type} {client.api_key}"}
                )
                if response.status_code != 401:
                    response.raise_for_status()
                    buf.write(response.content)
                    break
            else:
                response.raise_for_status()
                buf.write(response.content)
    except TypeError:
        # Some SDKs require a file path; fall back to tmp file then read back
        tmp = Path(f"snapshot_{project_id}_{snap_id}.zip")
        try:
            if hasattr(client, 'projects') and hasattr(client.projects, 'exports'):
                client.projects.exports.download(id=project_id, export_id=snap_id, path=str(tmp))
            else:
                import requests
                # Try Bearer token first (LS 1.20+), then Token (legacy)
                for auth_type in ["Bearer", "Token"]:
                    response = requests.get(
                        f"{client.url}/api/projects/{project_id}/exports/{snap_id}/download/",
                        headers={"Authorization": f"{auth_type} {client.api_key}"}
                    )
                    if response.status_code != 401:
                        response.raise_for_status()
                        tmp.write_bytes(response.content)
                        break
                else:
                    response.raise_for_status()
                    tmp.write_bytes(response.content)
            buf = io.BytesIO(tmp.read_bytes())
        finally:
            try:
                tmp.unlink()
            except Exception:
                pass

    buf.seek(0)
    with zipfile.ZipFile(buf) as zf:
        # Heuristics: try common names first
        candidate_names = [
            "tasks.json",
            "result.json",
            "export.json",
            "project.json",  # fallback (may contain metadata, not tasks)
        ]
        json_bytes = None
        for name in candidate_names:
            try:
                json_bytes = zf.read(name)
                break
            except KeyError:
                continue
        if json_bytes is None:
            # Fallback: first .json in the archive
            for name in zf.namelist():
                if name.lower().endswith(".json"):
                    json_bytes = zf.read(name)
                    break
        if json_bytes is None:
            raise RuntimeError("No JSON file found in snapshot ZIP")

    try:
        data = json.loads(json_bytes.decode("utf-8"))
    except Exception:
        data = json.loads(json_bytes)

    # Some exports wrap tasks inside a dict; try to detect
    if isinstance(data, dict):
        for key in ("tasks", "result", "items", "data"):
            if key in data and isinstance(data[key], list):
                data = data[key]
                break
    if not isinstance(data, list):
        raise RuntimeError("Snapshot JSON did not contain a list of tasks")
    return data


# =========================
# Rewriters & merge
# =========================

def apply_key_renames(d: Dict[str, Any], renames: Dict[str, str]) -> Dict[str, Any]:
    out = dict(d)
    for old, new in renames.items():
        if old in out:
            if new == "":
                # delete field
                out.pop(old, None)
            elif new != old:
                out[new] = out.pop(old)
    return out


def apply_prefix_url(value: Any, base: str, strip_dirs: bool) -> Any:
    if not isinstance(value, str):
        return value
    v = value
    if strip_dirs:
        v = Path(v).name
    if base.endswith("/"):
        return base + v
    else:
        return base + "/" + v


def apply_regex(value: Any, pattern: str, repl: str) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return re.sub(pattern, repl, value)
    except re.error:
        return value


def rewrite_task_data(
    task: Dict[str, Any],
    renames: Dict[str, str],
    prefix_field: Optional[str],
    base_url: Optional[str],
    strip_dirs: bool,
    regex_field: Optional[str],
    regex_pattern: Optional[str],
    regex_repl: Optional[str],
) -> Dict[str, Any]:
    data = dict(task.get("data", {}))
    data = apply_key_renames(data, renames)

    if prefix_field and base_url and prefix_field in data and isinstance(data[prefix_field], str):
        data[prefix_field] = apply_prefix_url(data[prefix_field], base_url, strip_dirs)

    if regex_field and regex_pattern is not None and regex_repl is not None:
        if regex_field in data:
            data[regex_field] = apply_regex(data[regex_field], regex_pattern, regex_repl)

    new_task = dict(task)
    new_task["data"] = data
    return new_task


def stable_key(task: Dict[str, Any], dedup_field: Optional[str]) -> str:
    data = task.get("data", {})
    if dedup_field and dedup_field in data and data[dedup_field] not in (None, ""):
        return str(data[dedup_field])
    blob = json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha1(blob).hexdigest()


def concat_and_dedup(
    lists: List[List[Dict[str, Any]]],
    dedup_field: Optional[str]
) -> Tuple[List[Dict[str, Any]], int]:
    seen = set()
    merged: List[Dict[str, Any]] = []
    dropped = 0
    for L in lists:
        for t in L:
            k = stable_key(t, dedup_field)
            if k in seen:
                dropped += 1
                continue
            seen.add(k)
            merged.append(t)
    return merged, dropped


def create_project(client, title: str, label_config: str, description: str = "") -> int:
    try:
        # Try modern SDK first
        if hasattr(client, 'projects') and hasattr(client.projects, 'create'):
            p = client.projects.create(title=title, label_config=label_config, description=description)
        elif hasattr(client, 'create_project'):
            p = client.create_project(title=title, label_config=label_config, description=description)
        else:
            # Fallback to direct API call
            import requests
            # Try Bearer token first (LS 1.20+), then Token (legacy)
            for auth_type in ["Bearer", "Token"]:
                response = requests.post(
                    f"{client.url}/api/projects/",
                    headers={"Authorization": f"{auth_type} {client.api_key}"},
                    json={
                        'title': title,
                        'label_config': label_config,
                        'description': description
                    }
                )
                if response.status_code != 401:
                    response.raise_for_status()
                    p = response.json()
                    break
            else:
                response.raise_for_status()
                p = response.json()
        
        return int(_safe_attr(p, "id"))
    except Exception as e:
        raise RuntimeError(f"Failed to create project: {e}")


def import_in_batches(client, project_id: int, items: List[Dict[str, Any]], batch: int = 1000, progress=None):
    total = len(items)
    sent = 0
    for i in range(0, total, batch):
        payload = items[i : i + batch]
        try:
            # Try modern SDK first
            if hasattr(client, 'projects') and hasattr(client.projects, 'import_tasks'):
                client.projects.import_tasks(id=project_id, request=payload, return_task_ids=False)
            elif hasattr(client, 'import_tasks'):
                client.import_tasks(project_id, payload)
            else:
                # Fallback to direct API call
                import requests
                # Try Bearer token first (LS 1.20+), then Token (legacy)
                for auth_type in ["Bearer", "Token"]:
                    response = requests.post(
                        f"{client.url}/api/projects/{project_id}/import",
                        headers={"Authorization": f"{auth_type} {client.api_key}"},
                        json=payload
                    )
                    if response.status_code != 401:
                        response.raise_for_status()
                        break
                else:
                    response.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Failed to import batch {i//batch + 1}: {e}")
            
        sent += len(payload)
        if progress is not None:
            progress.progress(min(int(sent / total * 100), 100), text=f"Imported {sent}/{total}")


def projects_dataframe(projects: List[Any]) -> pd.DataFrame:
    rows = []
    for p in projects:
        rows.append(
            dict(
                id=_safe_attr(p, "id"),
                title=_safe_attr(p, "title"),
                description=_safe_attr(p, "description"),
                created_at=_safe_attr(p, "created_at"),
                updated_at=_safe_attr(p, "updated_at"),
                task_number=_safe_attr(p, "task_number"),
                annotation_number=_safe_attr(p, "annotation_number"),
            )
        )
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def get_project_summary(client, project_id: int) -> Dict[str, Any]:
    """Get detailed project summary including accurate annotation count"""
    try:
        project = get_project(client, project_id)
        
        # Get accurate task and annotation counts
        task_count = 0
        annotation_count = 0
        
        try:
            # Try to get summary from project first
            task_count = _safe_attr(project, "task_number", 0) or 0
            annotation_count = _safe_attr(project, "annotation_number", 0) or 0
            
            # If annotation count is 0 or None, do manual count
            if annotation_count == 0:
                st.info(f"Counting annotations for project {project_id}...")
                annotation_count = 0
                task_count = 0
                
                for task in tasks_iter(client, project_id, fields="annotations", page_size=1000):
                    task_count += 1
                    annotations = _safe_attr(task, "annotations", [])
                    if annotations:
                        annotation_count += len(annotations)
        except Exception as e:
            st.warning(f"Could not count annotations for project {project_id}: {e}")
        
        return {
            "id": _safe_attr(project, "id"),
            "title": _safe_attr(project, "title"),
            "description": _safe_attr(project, "description"),
            "task_count": task_count,
            "annotation_count": annotation_count,
            "label_config": label_config_of(project)
        }
    except Exception as e:
        return {
            "id": project_id,
            "title": f"Error loading project {project_id}",
            "description": str(e),
            "task_count": 0,
            "annotation_count": 0,
            "label_config": ""
        }


# =========================
# UI
# =========================
st.set_page_config(page_title="Label Studio Project Tool", page_icon="🧩", layout="wide")

st.title("🧩 Label Studio Project Tool")
st.caption("Query projects • Export (stream or snapshot) • Field rewrite • Combine • Create merged project")

with st.sidebar:
    st.subheader("🔐 Connect")
    base_url = st.text_input("Base URL", value="http://localhost:8080")
    api_key = st.text_input("API Key (Personal Token)", type="password")
    connect_btn = st.button("Connect", type="primary")

if "client" not in st.session_state and connect_btn:
    try:
        st.session_state.client = connect_ls(base_url.strip(), api_key.strip())
        st.success("Connected.")
    except Exception as e:
        st.error(str(e))

client = st.session_state.get("client")
if not client:
    st.info("Enter your Label Studio URL and API Key in the sidebar to get started.")
    st.stop()

# Initialize session state for projects
if "projects_loaded" not in st.session_state:
    st.session_state.projects_loaded = False
if "projects_list" not in st.session_state:
    st.session_state.projects_list = []
if "selected_project_details" not in st.session_state:
    st.session_state.selected_project_details = {}
if "config_compatible" not in st.session_state:
    st.session_state.config_compatible = False
if "exported_data" not in st.session_state:
    st.session_state.exported_data = {"merged": [], "exports": [], "dropped": 0}

# Load projects button
st.subheader("📋 Projects")
col1, col2 = st.columns([1, 3])
with col1:
    load_projects_btn = st.button("🔄 Load Projects", type="primary")
with col2:
    if st.session_state.projects_loaded:
        st.success(f"Loaded {len(st.session_state.projects_list)} projects")
    else:
        st.info("Click 'Load Projects' to view available projects")

if load_projects_btn:
    try:
        with st.spinner("Loading projects..."):
            projs = list_projects(client)
            st.session_state.projects_list = projs
            st.session_state.projects_loaded = True
            st.rerun()
    except Exception as e:
        st.error(f"Failed to load projects: {e}")
        st.stop()

if st.session_state.projects_loaded:
    df = projects_dataframe(st.session_state.projects_list)
    st.dataframe(df, use_container_width=True, height=320)
    
    proj_options = {f'[{int(_safe_attr(p,"id"))}] {_safe_attr(p,"title")}': int(_safe_attr(p,"id")) for p in st.session_state.projects_list}
else:
    proj_options = {}
    st.info("Load projects first to continue.")
    st.stop()

st.divider()
st.subheader("🧮 Export & Combine")

colA, colB, colC = st.columns([1.2, 1.2, 1])
with colA:
    selected_labels = st.multiselect("Select source projects (2+ for merge)", list(proj_options.keys()))
    
    # Show details for selected projects
    if selected_labels:
        st.write("**Selected Projects Details:**")
        get_details_btn = st.button("📊 Get Detailed Counts")
        
        if get_details_btn:
            selected_ids = [proj_options[label] for label in selected_labels]
            with st.spinner("Getting project details..."):
                for project_id in selected_ids:
                    if project_id not in st.session_state.selected_project_details:
                        details = get_project_summary(client, project_id)
                        st.session_state.selected_project_details[project_id] = details
        
        # Display cached details
        total_tasks = 0
        total_annotations = 0
        for label in selected_labels:
            project_id = proj_options[label]
            if project_id in st.session_state.selected_project_details:
                details = st.session_state.selected_project_details[project_id]
                tasks = details['task_count']
                annotations = details['annotation_count']
                total_tasks += tasks
                total_annotations += annotations
                st.write(f"• {details['title']}: {tasks} tasks, {annotations} annotations")
        
        if total_tasks > 0:
            st.write(f"**Total: {total_tasks} tasks, {total_annotations} annotations**")

with colB:
    st.write("**Quick Export Options:**")
    use_snapshot_quick = st.checkbox("Use snapshot export", value=False, key="quick_snapshot")
    include_annotations_quick = st.checkbox("Include annotations", value=True, key="quick_annotations")
    
with colC:
    st.write("**Status:**")
    if len(selected_labels) >= 2:
        st.success(f"✅ {len(selected_labels)} projects selected")
        if st.session_state.get('config_compatible', False):
            st.success("✅ Configs compatible")
        else:
            st.warning("⚠️ Check config compatibility")
    else:
        st.info("Select 2+ projects")
    
    # Show export status
    merged_count = len(st.session_state.exported_data.get("merged", []))
    if merged_count > 0:
        st.success(f"✅ {merged_count} tasks exported")

# ---- Tabbed interface for better organization ----
tab1, tab2, tab3 = st.tabs(["📤 Export & Merge", "✏️ Field Rewriter", "🔧 Advanced Options"])

with tab1:
    export_btn = st.button("Export selected ➜ Apply rewrites ➜ JSON (preview below)", type="primary")

with tab2:
    st.markdown("### Configure field transformations (applied before de-dup & import)")
    col1, col2, col3 = st.columns([1.2, 1, 1])
    with col1:
        renames_str = st.text_input("Key renames (comma-separated 'old:new')", value="file_upload:", help="Example: file_upload:image, filepath:image")
    with col2:
        prefix_field = st.text_input("Prefix URL: field name", value="image")
        base_url = st.text_input("Base URL (e.g., https://storage.googleapis.com/bucket)", value="")
    with col3:
        strip_dirs = st.checkbox("Strip directories before prefix", value=True)

    col4, col5 = st.columns([1, 1])
    with col4:
        regex_field = st.text_input("Regex replace: field name", value="")
    with col5:
        regex_pattern = st.text_input("Pattern", value="")
        regex_repl = st.text_input("Replacement", value="")

with tab3:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Export Options")
        use_snapshot = st.checkbox("Use snapshot export (recommended for large projects)", value=False)
        include_annotations = st.checkbox("Include annotations (stream mode)", value=True)
        include_predictions = st.checkbox("Include predictions (stream mode)", value=False)
    
    with col2:
        st.subheader("Deduplication")
        dedup_field = st.text_input("De-dup field in data (optional)", value="image", help="e.g., 'image', 'text', 'audio'. Leave empty to hash the data dict.")

merged: List[Dict[str, Any]] = []
dropped = 0
exports: List[List[Dict[str, Any]]] = []

# Parse renames
renames: Dict[str, str] = {}
if renames_str.strip():
    for part in [p.strip() for p in renames_str.split(",") if p.strip()]:
        if ":" in part:
            old, new = part.split(":", 1)
            renames[old.strip()] = new.strip()

if export_btn:
    if not selected_labels:
        st.warning("Select at least one source project.")
    else:
        # Use values from the appropriate tabs
        use_snapshot = st.session_state.get('quick_snapshot', use_snapshot)
        include_annotations = st.session_state.get('quick_annotations', include_annotations)
        
        ids = [proj_options[k] for k in selected_labels]
        exports = []
        
        # Create progress container
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
        try:
            for i, (pid, label) in enumerate(zip(ids, selected_labels)):
                progress = (i / len(ids)) * 0.8  # Reserve 20% for post-processing
                progress_bar.progress(progress)
                status_text.text(f"Exporting project {i+1}/{len(ids)}: {label}")
                
                if use_snapshot:
                    data_list = build_export_snapshot(client, project_id=pid)
                else:
                    data_list = build_export_stream(
                        client,
                        project_id=pid,
                        include_annotations=include_annotations,
                        include_predictions=include_predictions,
                    )
                
                status_text.text(f"Applying rewrites to {len(data_list)} tasks from {label}...")
                
                # Apply rewrites to each task
                rewritten = [
                    rewrite_task_data(
                        t,
                        renames=renames,
                        prefix_field=prefix_field.strip() or None,
                        base_url=base_url.strip() or None,
                        strip_dirs=strip_dirs,
                        regex_field=regex_field.strip() or None,
                        regex_pattern=regex_pattern if regex_pattern else None,
                        regex_repl=regex_repl if regex_repl else None,
                    )
                    for t in data_list
                ]
                exports.append(rewritten)
            
            # Final processing
            progress_bar.progress(0.9)
            status_text.text("Merging and de-duplicating...")
            merged, dropped = concat_and_dedup(exports, dedup_field if dedup_field.strip() else None)
            
            progress_bar.progress(1.0)
            status_text.text("✅ Export complete!")
            
            # Store in session state
            st.session_state.exported_data = {
                "merged": merged, 
                "exports": exports, 
                "dropped": dropped
            }
            
            st.success(f"Exported and merged {len(merged)} tasks (dropped {dropped} duplicates)")
            st.rerun()  # Refresh to show the create button enabled
            
        except Exception as e:
            st.error(f"Export failed: {e}")
            st.session_state.exported_data = {"merged": [], "exports": [], "dropped": 0}

if exports:
    left, right = st.columns([1, 1])
    with left:
        st.write("Per-project counts (after rewrites):")
        for lbl, items in zip(selected_labels, exports):
            st.write(f"• {lbl}: {len(items)} tasks")
        st.write(f"🧮 De-dup dropped: {dropped}")
        st.write(f"✅ Merged total: {len(merged)}")

    with right:
        st.write("Download merged JSON:")
        merged_json = json.dumps(merged, ensure_ascii=False).encode("utf-8")
        st.download_button(
            "⬇️ Download merged.json",
            merged_json,
            file_name="merged.json",
            mime="application/json",
        )
        # Show a small preview row
        if merged:
            st.write("Preview (first item):")
            st.json(merged[0])
elif st.session_state.exported_data["merged"]:
    # Show results from session state if available
    merged = st.session_state.exported_data["merged"]
    exports = st.session_state.exported_data["exports"] 
    dropped = st.session_state.exported_data["dropped"]
    
    left, right = st.columns([1, 1])
    with left:
        st.write("**Cached Export Results:**")
        st.write(f"🧮 De-dup dropped: {dropped}")
        st.write(f"✅ Merged total: {len(merged)}")

    with right:
        st.write("Download merged JSON:")
        merged_json = json.dumps(merged, ensure_ascii=False).encode("utf-8")
        st.download_button(
            "⬇️ Download merged.json",
            merged_json,
            file_name="merged.json",
            mime="application/json",
        )
        if merged:
            st.write("Preview (first item):")
            st.json(merged[0])

st.divider()
st.subheader("🆕 Create Merged Project")

col1, col2 = st.columns([1.6, 1])
with col1:
    dst_title = st.text_input("New project title", value="Merged Project")
    dst_description = st.text_area(
        "Description (optional)",
        value="Auto-merged from selected source projects. Originals left unchanged.",
    )
with col2:
    batch_size = st.number_input("Import batch size", min_value=100, max_value=50000, step=100, value=2000)

# Enable create button if we have selected projects and exported data
merged = st.session_state.exported_data.get("merged", [])
exports = st.session_state.exported_data.get("exports", [])
dropped = st.session_state.exported_data.get("dropped", 0)

# Check all prerequisites
has_projects = len(selected_labels) >= 2
has_exported_data = len(merged) > 0
has_compatible_config = st.session_state.get('config_compatible', False)

can_create = has_projects and has_exported_data and has_compatible_config

if not has_projects:
    button_help = "Select at least 2 projects to merge"
elif not has_compatible_config:
    button_help = "Check label config compatibility first"
elif not has_exported_data:
    button_help = "Export projects first to enable merge"
else:
    button_help = f"Create new project with {len(merged)} merged tasks"

create_btn = st.button(
    "Create project & import merged tasks", 
    type="primary", 
    disabled=not can_create,
    help=button_help
)

def normalize_label_config(config: str) -> str:
    """Normalize label config for comparison by removing whitespace and formatting differences"""
    if not config:
        return ""
    
    import re
    # Remove extra whitespace, newlines, and normalize spacing
    normalized = re.sub(r'\s+', ' ', config.strip())
    # Remove spaces around tags and attributes
    normalized = re.sub(r'>\s+<', '><', normalized)
    normalized = re.sub(r'\s*=\s*', '=', normalized)
    # Sort attributes within tags for consistent comparison
    return normalized.lower()


# Check label config compatibility when projects are selected
if len(selected_labels) >= 2:
    st.markdown("### 🔍 Label Config Compatibility Check")
    check_config_btn = st.button("🔍 Check Label Config Compatibility")
    
    if check_config_btn:
        selected_ids = [proj_options[label] for label in selected_labels]
        with st.spinner("Checking label configurations..."):
            configs = []
            for pid in selected_ids:
                try:
                    p = get_project(client, pid)
                    cfg = label_config_of(p) or ""
                    configs.append((pid, cfg.strip(), normalize_label_config(cfg)))
                except Exception as e:
                    st.error(f"Failed to get config for project {pid}: {e}")
                    configs.append((pid, "", ""))
            
            # Check if all normalized configs are the same
            if not configs:
                st.error("No configurations found")
                st.session_state.config_compatible = False
            else:
                first_normalized = configs[0][2]
                all_same = all(normalized == first_normalized for _, _, normalized in configs)
                
                if all_same:
                    st.success("✅ All selected projects have compatible label configurations!")
                    st.session_state.config_compatible = True
                else:
                    st.error("❌ Selected projects have different label configurations!")
                    st.session_state.config_compatible = False
                    
                    # Show differences
                    st.write("**Configuration comparison:**")
                    for i, (pid, original, normalized) in enumerate(configs):
                        project_title = next((label for label in selected_labels if proj_options[label] == pid), f"Project {pid}")
                        with st.expander(f"{project_title} - Config Length: {len(original)} chars", expanded=False):
                            if original:
                                st.code(original, language="xml")
                            else:
                                st.write("(empty or no config)")

if create_btn:
    # Validate prerequisites
    if len(selected_labels) < 2:
        st.error("Please select at least 2 projects to merge.")
        st.stop()
    
    if not st.session_state.get('config_compatible', False):
        st.error("Please check label config compatibility first.")
        st.stop()
    
    if len(merged) == 0:
        st.error("Please export projects first.")
        st.stop()

    # Get label config from first project
    first_id = proj_options[selected_labels[0]]
    p_first = get_project(client, first_id)
    cfg_first = label_config_of(p_first) or ""
    
    if not cfg_first.strip():
        st.warning("Warning: First project has empty label config. Proceeding anyway.")

    try:
        with st.spinner("Creating project..."):
            dst_id = create_project(client, dst_title, cfg_first, dst_description)
        st.success(f"Created project id={dst_id}")

        warn = (
            "Heads-up: if your tasks used `file_upload` in `data`, those file IDs do not carry over. "
            "Prefer URLs or connected cloud storage paths (use the Field Rewriter above)."
        )
        st.caption(warn)

        progress = st.progress(0, text="Starting import...")
        import_in_batches(client, dst_id, merged, batch=batch_size, progress=progress)
        progress.progress(100, text="Done")
        st.success(f"Imported {len(merged)} tasks into project {dst_id}.")
    except Exception as e:
        st.error(str(e))
