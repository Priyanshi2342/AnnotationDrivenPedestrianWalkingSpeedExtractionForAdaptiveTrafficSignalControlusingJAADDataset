
# 🚦 Annotation-Driven Pedestrian Walking Speed Detection

*Adaptive Traffic Signal Control using JAAD Dataset (Project-Based Research)*

## 📌 Overview

This project introduces a lightweight, annotation-only pipeline to estimate pedestrian walking speed at road intersections using the **JAAD dataset**. Instead of running real-time object-detection or deep-learning models, the system directly processes existing XML annotations to extract centroid trajectories from bounding boxes and compute frame-wise displacement as a proxy for walking speed.

Slow pedestrians are flagged using a predefined threshold, and **FFmpeg automatically generates 5-second evidence clips** for result validation and explainability.

## 🎯 Problem Statement

Standard pedestrian traffic signals allocate **fixed crossing time**, which can be unsafe for:

* Elderly individuals
* Children
* Visually impaired or slow-moving pedestrians

Most intelligent traffic research focuses on **detection, tracking, or behavior prediction**, but rarely uses **walking speed as a real trigger for traffic-control decisions**. This project bridges that gap by demonstrating reliable speed estimation from annotations and forming a base for adaptive signal-time extension.

## 🛠️ Pipeline Architecture

```
JAAD Videos + XML Annotations  
        ↓  
Parse Annotation Files  
        ↓  
Extract Bounding Box Centroids  
        ↓  
Compute Frame-to-Frame Displacement  
        ↓  
Classify Slow Pedestrians (S < 1.4)  
        ↓  
Generate Evidence Clips (FFmpeg)  
```

## 📊 Dataset & Performance

| Parameter                      | Value                                 |
| ------------------------------ | ------------------------------------- |
| XML Annotation Files Processed | 326                                   |
| Matched Video Clips Available  | 17                                    |
| Videos with Slow Pedestrians   | 2                                     |
| Evidence Clips Generated       | 2                                     |
| Speed Metric                   | Pixel displacement per frame (30 FPS) |

## 🔍 Key Features

* **No ML model training or inference**
* **Fully deterministic and reproducible**
* **Uses only dataset annotations**
* **Generates explainable evidence clips**
* **Low compute footprint**
* **Real-world integration potential**

## 💡 Use Cases

* Adaptive pedestrian crossing time extension
* Intelligent traffic prototyping
* Dataset-level motion analysis
* Annotation-based trajectory extraction research

## ⚡ FFmpeg Evidence Generation (used internally)

Clips are generated for validation only, using:

```
ffmpeg -ss <timestamp> -t 5 -i input.mp4 output_clip.mp4
```

## 🧪 Results Discussion

The project proves that:

* Pedestrian walking speed can be reliably approximated using **only centroid motion from annotations**
* Speed can be used as an **actionable safety signal**
* Evidence clips allow transparent validation without live CV models

## 🚧 Limitations

* Speed is approximated in **pixel units**, not meters/second
* Depends on availability of **pre-annotated datasets**
* Not yet deployed in real-time CCTV feeds

## 🔮 Future Enhancements

* Real-time integration using **YOLO + DeepSORT**
* Adaptive traffic-signal controller triggered by walking speed
* Pose-based posture correctness evaluation
* IoT/Edge deployment at intersections

## 👤 Author

**Priyanshi Sharma**
*Computer Science & Engineering (CSE)*
