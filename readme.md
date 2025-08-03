# Raceline Editor

A tool for editing and modifying racing lines through visual map manipulation using GIMP.

## Project Structure

```
raceline_editor/
├── original_racinglines/     ← Place your input racingline files here
├── mod_maps/                 ← Modified maps go here (e.g. mod_map.png)
├── output_racinglines/       ← Final extracted racing lines output
├── racingline_drawer/src/
│   └── drawer.py            ← Drawer script
├── path_extractor/src/
│   └── extractor.py         ← Extractor script
└── README.md
```

## Dependencies

The project uses the following Python libraries:
- `math` (hypot)
- `shutil`
- `queue` (Queue)
- `PIL` (Pillow)
- `yaml`
- `csv`
- `argparse`
- `cv2` (OpenCV)
- `pandas`
- `os`

Install the required packages:
```bash
pip install pillow pyyaml opencv-python pandas
```

## Usage Instructions

### Step 1: Prepare Input Files
Place your input racingline files inside the `original_racinglines/` directory.

### Step 2: Generate Visual Map
Run the drawer script to create a visual representation of your racing line:
```bash
python3 -m racingline_drawer.src.drawer
```
![Alt Text](assets/mod_map.png)

### Step 3: Edit in GIMP
1. Open GIMP
2. Open the generated `mod_map.png` file from the `mod_maps/` directory

![Alt Text](assets/wrong_line.png)

### Step 4: Handle Yellow Configured Pixel
⚠️ **Important**: If your path is revolving around the yellow 'configured' pixel, you need to relocate it to prevent the modified path from creating a bridge between the yellow pixel and the path.

![Alt Text](assets/fixing.png)

### Step 5: Edit the Path
Carefully place your pixels in the following order:
1. **Start pixel** - Mark the beginning of your modified path
2. **Path pixels** - Draw your desired racing line
3. **End pixel** - Mark the end of your modified path

**Critical Requirements:**
- All pixels must be close to each other within the 8 directions (horizontally, vertically, and diagonally adjacent)
- Ensure continuity between start, path, and end pixels
- No gaps should exist in your pixel chain

### Step 6: Extract Modified Racing Line
Run the extractor script to generate the final racing line:
```bash
python3 -m path_extractor.src.extractor
```

The output will be saved in the `output_racinglines/` directory.

### Step 7: Verification (Optional)
To verify your modifications:
1. Copy the output racingline from `output_racinglines/` to `original_racinglines/`
2. Run the drawer script again:
   ```bash
   python3 -m racingline_drawer.src.drawer
   ```
3. Check the generated visual map to confirm your changes

## Tips
- Always ensure pixel connectivity when drawing your path in GIMP
- Use the zoom feature in GIMP for precise pixel placement
- Save your work frequently when editing in GIMP
- Keep backups of your original racingline files before making modifications

## Troubleshooting
- If the extractor fails, check that all pixels in your path are properly connected
- Ensure the yellow configured pixel is not interfering with your path
- Verify that start and end pixels are correctly placed and connected to the path