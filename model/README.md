# AI Model

## Overview

This directory contains the **pre-trained and optimized AI models** used for real-time inference on the **MaixCam NPU**. These models are **not trained on-device**; all training and conversion steps are performed offline.

The models are used exclusively for **object detection of the levitating ball**, providing the visual feedback required for closed-loop control.

---

## Model Formats

The following model formats are included:

* **`.mud`**
  Runtime model format compatible with **MaixPy v3**. This is the file loaded directly by the embedded application.

* **`.cvimodel`**
  Compiled model format optimized for the MaixCam NPU. Used internally by the runtime for accelerated inference.

---

## Model Description

* **Architecture:** YOLOv5
* **Task:** Single-class object detection (ball)
* **Output:** Bounding box coordinates and confidence score

The bounding box width is used to estimate the distance to the object using a pinhole camera model.

---

## Dataset and Training

The model was trained using a **diverse dataset** captured inside the wind tunnel:

* Multiple distances along the tube
* Different lighting conditions
* Variations in background and reflections

This dataset diversity improves **robustness to lighting disturbances** and ensures reliable detection under non-ideal conditions.

---

## Notes

* Training scripts and raw datasets are **not included** in this repository.
* Models are provided for **demonstration, validation, and deployment** purposes only.
* If you plan to retrain or modify the model, ensure compatibility with MaixCam-supported formats.

