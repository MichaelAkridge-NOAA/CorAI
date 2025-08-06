# Models
## Model Zoo
Save pretrained models, model checkpoints, and training logs here. Document model architectures and usage instructions as needed.

## Model Dev Plan

```mermaid
graph TD
  %% DATA SOURCES
  CNTrain[CN Training Data]
  MARTrain[MAR PT Training Data]
  VRChunk[VR Chunk Data]
  BleachData[Bleaching Data]

  %% MODELS
  CNClassifier["CN PT Classifier"]
  T3Model["T3 PT YOLO Model"]
  T3PSEG["T3PSEG Segmentation Model"]
  SAMModels["SAM Models (SAM1/SAM2/SAM3)"]
  Segments["Segments (Segmask A/B)"]

  %% WORKFLOW
  CNTrain --> CNClassifier
  MARTrain --> T3Model
  T3Model -->|Deploy on FY22| T3PSEG
  T3PSEG -->|Train + Validate| Segments
  VRChunk -->|Validate| Segments
  BleachData -->|Train/Validate| T3Model

  Segments -->|Compare| Voting["Segmask Voting"]
  Voting -->|Good?| Deploy["Deploy on FY25 Images"]
  Deploy --> Ortho["Ortho Segments A/B"]
  Ortho -->|Compare to VRChunk| Metrics["Performance Metric"]

  %% EVALUATION
  CNClassifier --> EvalCN["Confusion Matrix / ROC AUC"]
  T3Model --> EvalT3["Compare Test vs CN Performance"]

  %% AUX / PATCH LOGIC
  Subgraph["Quadrant Census Plan"]
  Subgraph --> T1["T1: 75% Target Inclusion"]
  Subgraph --> T2["T2: Missed Targets / Recruits"]
  Subgraph --> Census["Census Patch-Level Expansion"]

  %% OUTPUT
  Metrics --> FinalCheck["Final Model Evaluation"]
```
## AI/ML Workflow Plan – Steps (Right Side)

- [x] 0. MARIAN TRAIN DATA ✅ `A1`
- [x] 1. VR CHUNK DATA ✅ `A1`
- [x] 2. BLEACHING DATA ✅ `A1`
- [x] 3. BLEACHING MODEL ✅ `89%`

## Training & Deployment Workflow

1. Train T3 YOLO PT model → `T3P`
   - with T-T Split v1.7 (FY22)
   - ☐ Compare test performance to CN performance
   - Ensure no CN-trained images included

2. Deploy `YT3P` on FY22 (`PQ`)
   - → Dense PT dataset

3. Create "wrapper" dense PT dataset
   - 3.1. YT3P Dense Segmask (FY22 PQ)
   - 3.2. Validate on VRChunk (**METRIC**)

4. Train YT3PSEG Model

5. Deploy YT3PSEG on VRChunk (**METRIC**)
   - Good?
     - If ✔️:
       - 5.1 Deploy on FY25 images → generate FY25 ortho segmask A
     - If ❌:
       - 5.2 Deploy on FY25 orthos → generate FY25 ortho segmask B
       - 5.3 Compare ortho segmask A/B to VRChunk (**METRIC**)

6. All 4 SAM...


```mermaid
flowchart TD
  %% DATA SOURCES
  CNTrain["CN Training Data"]
  MARTrain["MAR PT Training Data"]
  VRChunk["VR Chunk Data"]
  BleachData["Bleaching Data"]

  %% CLASSIFIER
  CNTrain --> CNClassifier["CN PT Classifier"]
  CNClassifier --> EvalCN["Evaluate: Confusion Matrix + ROC AUC"]

  %% T3 MODEL TRAINING
  MARTrain --> T3Model["T3 PT YOLO Model"]
  T3Model --> YT3P["Deploy YT3P on FY22"]
  YT3P --> DensePT["Dense PT Dataset"]

  %% SEGMENTATION
  DensePT --> Wrapper["Wrapper Dataset"]
  Wrapper --> YT3PSEG["Train YT3PSEG Model"]
  YT3PSEG --> SegOutput["Segmentation Output - Segmask A and B"]
  SegOutput --> Voting["Voting + Comparison"]

  %% DEPLOYMENT
  Voting -->|Good| DeployA["Deploy on FY25 Images → Segmask A"]
  Voting -->|Not Good| DeployB["Deploy on FY25 Orthos → Segmask B"]
  DeployA --> Compare["Compare to VRChunk Metrics"]
  DeployB --> Compare

  %% SAM
  T3Model --> SAM["SAM Models (SAM1, SAM2, SAM3)"]
  SAM --> SegOutput

```



```mermaid
flowchart TD
  %% DATA SOURCES (Rectangles)
  CNTrain[CN Training Data]
  MARTrain[MAR PT Training Data]
  VRChunk[VR Chunk Data]
  BleachData[Bleaching Data]

  %% MODELS (Diamonds)
  CNClassifier{CN PT Classifier}
  T3Model{T3 PT YOLO Model}
  YT3P{YT3P Deployment}
  YT3PSEG{YT3PSEG Segmentation Model}
  SAM{SAM Models - SAM1, SAM2, SAM3}

  %% OTHER / PROCESSES (Rounded boxes)
  EvalCN(CN Evaluation - ROC AUC and Confusion Matrix)
  DensePT(Dense PT Dataset)
  Wrapper(Wrapper Dataset)
  SegOutput(Segmentation Output - Segmask A and B)
  Voting(Voting and Comparison)
  DeployA(Deploy FY25 Images - Segmask A)
  DeployB(Deploy FY25 Orthos - Segmask B)
  Compare(Final Comparison with VRChunk)

  %% FLOW
  CNTrain --> CNClassifier --> EvalCN
  MARTrain --> T3Model --> YT3P --> DensePT --> Wrapper --> YT3PSEG
  YT3PSEG --> SegOutput --> Voting
  Voting -->|Good| DeployA --> Compare
  Voting -->|Not Good| DeployB --> Compare
  T3Model --> SAM --> SegOutput
  VRChunk --> Compare
  BleachData --> T3Model
```
