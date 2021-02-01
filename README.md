# README

See discourse link [here, regarding blade envelopes](https://discourse.equadratures.org/t/blade-envelopes-3d-visualisation/105) visualisation files

# YouTube Video

https://www.youtube.com/watch?v=SmGCCoMWJxU

# Files

- `baseline-frompyscript.csv`:
  - Baseline blade profile vertex locations
  
- `blade_envelopes.npz`:
  - Loss/mass flow invariant blade profiles vertex locations

- `blender-import-baseline-ply-and-create-polyline-simple.py`:
  - Blender python script to import above csv file to visualise baseline blade profile as mesh

- `create-splines-pure-blender-simple`:
  - Blender python script to import above npz file to visualise random blade profiles as meshes
  
- `final-splines-simple.blend`
  - Save file after running above scripts
  
- `PRGn-colourmap.npz`
  - Save of matplotlib `PRGn` colourmap as numpy array