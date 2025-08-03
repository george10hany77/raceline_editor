
---

```markdown
# 🏁 RaceLine Editor

**RaceLine Editor** is a lightweight toolkit that allows you to overlay, manually edit, and extract racing lines from map images for custom path optimization.

## 🧰 Requirements

- 🐍 Python 3.7+
- 🎨 [GIMP](https://www.gimp.org/) for manual pixel editing

## 📂 Folder Structure


raceline_editor/
├── original_racinglines/     ← Place your input racingline files here
├── mod_maps/                 ← Modified maps go here (e.g. mod_map.png)
├── output_racinglines/       ← Final extracted racing lines output
├── racingline_drawer/src/
│   └── drawer.py             ← Drawer script
├── path_extractor/src/
│   └── extractor.py          ← Extractor script
└── README.md


## 🚦 How to Use

Follow the steps below **in order**:

### 1️⃣ Place your input racingline

Put your 'csv' racingline file into:

original_racinglines/


### 2️⃣ Run the drawer script

python3 -m racingline_drawer.src.drawer


This generates a `mod_map.png` in `mod_maps/` with your racing line overlaid.

![drawnRacingline](assets/mod_map.png)

### 3️⃣ Open the image in GIMP

Launch GIMP and open:

mod_maps/mod_map.png


### 4️⃣ Avoid yellow pixels ⚠️

If your racingline **crosses any yellow "configured" pixel**, you must manually adjust it. These yellow pixels are reserved areas that should not be overridden.

🟡 Yellow = Off-limits

![yelloPixel](assets/wrong_line.png)

Make it like this:

![fixing](assets/fixing.png)

### 5️⃣ Mark the path manually

* Add **1 start pixel** (e.g. green)
* Draw a **continuous path** (e.g. purple)
* Add **1 end pixel** (e.g. blue)

> ✅ **All pixels must be adjacent in one of the 8 directions** — no gaps allowed!

🧭 Your path must be 8-connected (including diagonals).


### 6️⃣ Run the extractor script

python3 -m path_extractor.src.extractor

This extracts your manually edited path and saves the result in:

output_racinglines/

You get:

* A file with path coordinates


## 🛠️ Troubleshooting

| Problem                     | Fix                                                              |
| --------------------------- | ---------------------------------------------------------------- |
| ❌ Start/end pixel not found | Make sure they're unique, visible, and saved before closing GIMP |
| ❌ Path crosses yellow pixel | Carefully move it away using GIMP's tools                        |
| ❌ Disconnected path         | Ensure all pixels are 8-connected with no gaps                   |
| ❌ Output is empty or wrong  | Double-check pixel color, spacing, and map resolution            |

## 📌 Quick Command Recap

# Step 1: Draw racing line

python3 -m racingline_drawer.src.drawer

# Step 2: Edit mod_map.png in GIMP (no yellow pixels, 8-connected path)

# Step 3: Extract pixel path
python3 -m path_extractor.src.extractor

## 🤝 Contributions

Want to improve it?

* Automate yellow-pixel detection
* Add validation for pixel paths
* Customize start/end colors

Pull requests and ideas are welcome!

## ⚖️ License

MIT License

Copyright (c) 2025 George Hany

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Made with 💻 and 🏎️ by [@george10hany77](https://github.com/george10hany77)
