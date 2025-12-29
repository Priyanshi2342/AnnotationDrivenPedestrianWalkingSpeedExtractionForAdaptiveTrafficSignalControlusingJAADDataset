import os
import subprocess
import xml.etree.ElementTree as ET

# --- CONFIG ---
VIDEOS_DIR = "JAAD_clips"
ANNOTATIONS_DIR = "Annotations"
OUTPUT_DIR = "slow_pedestrian_clips"
SPEED_THRESHOLD = 2.5  # base threshold for slow movement
CLIP_LENGTH = 5        # seconds

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- XML PARSER ---
def parse_annotation(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    pedestrians = []

    for track in root.findall("track"):
        label = track.get("label", "").lower()
        if "pedestrian" in label or "person" in label:
            boxes = []
            for box in track.findall("box"):
                frame = int(box.get("frame", 0))
                xtl = float(box.get("xtl", 0))
                ytl = float(box.get("ytl", 0))
                xbr = float(box.get("xbr", 0))
                ybr = float(box.get("ybr", 0))
                x = (xtl + xbr) / 2
                y = (ytl + ybr) / 2
                boxes.append((frame, x, y))
            if boxes:
                pedestrians.append(boxes)
    return pedestrians

# --- SPEED CALC ---
def calc_speed(ped):
    if len(ped) < 2:
        return 0
    speeds = []
    for i in range(1, len(ped)):
        f1, x1, y1 = ped[i - 1]
        f2, x2, y2 = ped[i]
        dx = x2 - x1
        dy = y2 - y1
        dist = (dx ** 2 + dy ** 2) ** 0.5
        speeds.append(dist)
    return sum(speeds) / len(speeds)

# --- CLIP EXTRACTOR ---
def extract_clip(video_path, start_frame, fps=30):
    start_time = start_frame / fps
    out = os.path.join(
        OUTPUT_DIR, f"{os.path.basename(video_path).split('.')[0]}_{int(start_time)}s.mp4"
    )
    cmd = [
        "ffmpeg", "-ss", str(start_time),
        "-i", video_path,
        "-t", str(CLIP_LENGTH),
        "-c", "copy", "-y", out
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Extracted clip: {out}")

# --- MAIN LOGIC ---
matched = []
for ann in os.listdir(ANNOTATIONS_DIR):
    if ann.endswith(".xml"):
        video_name = ann.replace(".xml", ".mp4")
        video_path = os.path.join(VIDEOS_DIR, video_name)
        if os.path.exists(video_path):
            matched.append((ann, video_path))

print(f"\n🎯 Found {len(matched)} video–annotation pairs.\n")

for ann, video_path in matched:
    ann_path = os.path.join(ANNOTATIONS_DIR, ann)
    peds = parse_annotation(ann_path)

    if not peds:
        print(f"⚠  No pedestrians found in {ann}")
        continue

    speeds = [calc_speed(p) for p in peds]
    slowest_speed = min(speeds)
    slowest_ped = peds[speeds.index(slowest_speed)]

    print(f"📊 {ann} | Slowest pedestrian speed = {slowest_speed:.2f}")

    if slowest_speed < SPEED_THRESHOLD:
        print(f"🐢 Extracting clip (slow pedestrian detected!)")
        extract_clip(video_path, slowest_ped[0][0])
    else:
        print(f"🚶 All pedestrians fast in: {ann}")

print("\n✅ Done! Check 'slow_pedestrian_clips' for output videos.")