# CLIP-Guided Counterfactual Analysis of Affective Image Editing Stability

## 1. Project Overview

This project explores how low-level visual attributes influence the emotional perception of images. Instead of directly generating new images, the project performs counterfactual image editing by adjusting brightness, contrast, saturation, and color temperature. Then, CLIP image-text similarity is used to evaluate whether these edits improve the alignment between an image and a target emotion.head -20 README.md
tail -40 README.md

The main goal is not to build a universal emotional filter. Instead, this project analyzes whether fixed affective editing presets are stable across different images and emotional targets.

The project focuses on the following research question:

> Are fixed low-level visual editing strategies equally effective and stable for different emotional targets?

## 2. Motivation

Image emotion is influenced by both visual appearance and semantic content. Simple visual operations, such as darkening an image or increasing saturation, may strengthen some emotions, but they may not work equally well for all emotional targets.

For example, reducing brightness and saturation may make an image appear more lonely or scary, while increasing brightness may not always make an image appear happier. This suggests that affective image editing may be both emotion-dependent and image-dependent.

This project investigates this problem through CLIP-guided counterfactual experiments.

## 3. Method

For each input image and target emotion, the system generates several counterfactual versions of the image:

* original
* brightness_only
* contrast_only
* saturation_only
* temperature_only
* all_attributes

Each target emotion is mapped to a fixed visual editing preset. The editable visual attributes include:

* brightness
* contrast
* saturation
* color temperature

After generating the edited versions, CLIP is used to compute the similarity between each image version and a target text prompt, such as:

```text
a lonely image
a scary image
a romantic image
```

For each image-emotion pair, the image version with the highest CLIP similarity score is selected as the best edit.

The score improvement is defined as:

```text
best_improvement = best_score - original_score
```

This measures how much the best edited version improves the CLIP similarity score compared with the original image.

## 4. Target Emotions

The experiment uses six target emotions:

* happy
* lonely
* scary
* peaceful
* romantic
* hopeful

These emotions are selected to cover both positive and negative affective directions, as well as different visual styles.

## 5. Experimental Setup

The main experiment was conducted on:

* 100 input images
* 6 target emotions
* 6 image versions for each image-emotion pair
* 600 total image-emotion evaluation results

For each image-emotion pair, the project records:

* original CLIP score
* best edited CLIP score
* best edit type
* best improvement
* output CSV path
* output plot path

The main summary file is saved as:

```text
results_multi/all_images_all_emotions_summary.csv
```

## 6. Overall Results

The average best improvements across 100 images are shown below:

| Emotion  | Number of Images | Average Best Improvement | Max Improvement | Min Improvement |
| -------- | ---------------: | -----------------------: | --------------: | --------------: |
| lonely   |              100 |                  0.01185 |         0.03069 |         0.00000 |
| scary    |              100 |                  0.00916 |         0.02355 |         0.00000 |
| romantic |              100 |                  0.00420 |         0.01356 |         0.00000 |
| peaceful |              100 |                  0.00345 |         0.01150 |         0.00000 |
| happy    |              100 |                  0.00312 |         0.01145 |         0.00000 |
| hopeful  |              100 |                  0.00224 |         0.01001 |         0.00000 |

The results show that lonely and scary achieve the highest average improvements. This suggests that these negative emotions are more strongly affected by low-level visual attributes such as brightness, saturation, contrast, and color temperature.

In contrast, happy and hopeful show lower average improvements. This suggests that positive emotions may depend more on image semantics, such as objects, facial expressions, and scene content, rather than simple low-level visual editing.

## 7. Stability Analysis

The dominant best edit for each emotion is shown below:

| Emotion  | Dominant Best Edit |    Count | Ratio |
| -------- | ------------------ | -------: | ----: |
| lonely   | all_attributes     | 79 / 100 |  0.79 |
| scary    | all_attributes     | 64 / 100 |  0.64 |
| peaceful | all_attributes     | 43 / 100 |  0.43 |
| romantic | temperature_only   | 37 / 100 |  0.37 |
| hopeful  | all_attributes     | 29 / 100 |  0.29 |
| happy    | all_attributes     | 25 / 100 |  0.25 |

The lonely emotion shows the strongest stability. In 79% of the images, the combined all_attributes edit is selected as the best version. This indicates that lonely can be more consistently enhanced by combined low-level visual edits.

Scary also shows relatively strong stability, with all_attributes selected in 64% of images.

However, happy and hopeful have much lower dominant ratios, meaning that no single editing strategy consistently works well for these emotions. This supports the idea that affective editing is both emotion-dependent and image-dependent.

## 8. Best Edit Distribution

The best edit type distribution further shows that different emotions respond differently to the same set of editing operations.

For lonely, all_attributes is selected as the best edit in 79 images, which is much higher than all other edit types. For scary, all_attributes is also dominant, selected in 64 images.

For romantic, temperature_only is selected as the best edit in 37 images, while all_attributes is selected in 35 images. This suggests that romantic emotion may be especially sensitive to color temperature.

For happy and hopeful, the best edit types are more scattered. This means that fixed visual presets are less stable for these emotions.

## 9. Case Studies

Several representative cases were selected for closer inspection.

| Image    | Emotion  | Best Edit        | Original Score | Best Score | Improvement |
| -------- | -------- | ---------------- | -------------: | ---------: | ----------: |
| test_027 | lonely   | all_attributes   |         0.2075 |     0.2382 |      0.0307 |
| test_023 | lonely   | all_attributes   |         0.2054 |     0.2359 |      0.0304 |
| test_054 | scary    | all_attributes   |         0.2130 |     0.2365 |      0.0235 |
| test_023 | scary    | all_attributes   |         0.2050 |     0.2283 |      0.0232 |
| test_085 | romantic | temperature_only |         0.2225 |     0.2352 |      0.0127 |
| test_041 | hopeful  | all_attributes   |         0.2138 |     0.2238 |      0.0100 |
| test_001 | happy    | original         |         0.2272 |     0.2272 |      0.0000 |
| test_029 | hopeful  | original         |         0.2353 |     0.2353 |      0.0000 |

For the lonely target, test_027 shows the strongest improvement. The all_attributes edit increases the CLIP similarity score from 0.2075 to 0.2382, with an improvement of 0.0307.

For the scary target, test_054 also shows a clear improvement. The all_attributes edit increases the score from 0.2130 to 0.2365, with an improvement of 0.0235.

For the romantic target, test_085 is an interesting case. The best edit is temperature_only, increasing the score from 0.2225 to 0.2352. This suggests that romantic emotion may be especially sensitive to color temperature.

There are also cases where the original image is already the best version. For example, test_029 under the hopeful target selects original as the best version. These cases show that fixed visual editing does not always improve emotional alignment.

## 10. Key Findings

The experiment leads to several observations:

1. Fixed affective editing presets are not equally stable across emotions.
2. Lonely and scary are more consistently improved by combined low-level visual edits.
3. Romantic is relatively sensitive to color temperature.
4. Happy and hopeful are less stable and show weaker improvements.
5. Some images are already best aligned with the target emotion before editing.
6. Affective image editing is both image-dependent and emotion-dependent.

Overall, the results suggest that simple visual attributes can influence affective image perception, but their effectiveness depends heavily on the target emotion and the input image.

## 11. Limitations

This project uses CLIP similarity as the evaluation metric. Therefore, the results reflect CLIP's image-text alignment behavior rather than direct human emotional perception.

The editing operations are limited to low-level visual attributes, including brightness, contrast, saturation, and color temperature. More complex semantic changes, such as modifying facial expressions, changing objects, or altering scene structure, are not included.

The dataset contains 100 images, which is suitable for a small-scale exploratory experiment. However, larger and more diverse datasets would be needed for stronger conclusions.

The emotional presets are manually designed rather than learned automatically. This makes the method simple and interpretable, but also limits its adaptability.

## 12. Future Work

Future improvements could include:

* adding more target emotions
* testing different CLIP models
* comparing CLIP evaluation with human evaluation
* using image-adaptive editing instead of fixed presets
* learning emotion-specific editing parameters automatically
* adding semantic image editing methods
* building an interactive demo for emotion-guided image editing

## 13. How to Run

### 13.1 Activate the environment

```bash
cd ~/clip_affective_editing
source huiyan/bin/activate
```

### 13.2 Run a single-image experiment

```bash
python run_experiment.py --input images/test.jpg --emotion lonely
```

Optional custom prompt:

```bash
python run_experiment.py --input images/test.jpg --emotion lonely --prompt "a lonely image"
```

### 13.3 Run all emotions on one image

```bash
python run_all_emotions.py
```

### 13.4 Run the full multi-image experiment

Put input images into:

```text
images/multi
```

Then run:

```bash
python run_multi_images.py
```

This will generate the main summary file:

```text
results_multi/all_images_all_emotions_summary.csv
```

### 13.5 Analyze multi-image results

```bash
python analyze_multi_results.py
python plot_multi_analysis.py
```

The final analysis files include:

```text
results_multi/emotion_average_improvements.csv
results_multi/emotion_best_edit_counts.csv
results_multi/emotion_stability_analysis.csv
results_multi/emotion_average_improvements.png
results_multi/emotion_best_edit_counts.png
results_multi/emotion_stability_analysis.png
```

### 13.6 Inspect representative examples

```bash
python inspect_examples.py
python export_case_images.py
python summarize_case_studies.py
```

Representative case study outputs are saved in:

```text
case_studies/
```

## 14. Project Structure

```text
clip_affective_editing/
├── images/
│   ├── test.jpg
│   └── multi/
│       ├── test_001.jpg
│       ├── test_002.jpg
│       └── ...
│
├── results/
│   └── single-image experiment outputs
│
├── results_multi/
│   ├── all_images_all_emotions_summary.csv
│   ├── emotion_average_improvements.csv
│   ├── emotion_best_edit_counts.csv
│   ├── emotion_stability_analysis.csv
│   ├── emotion_average_improvements.png
│   ├── emotion_best_edit_counts.png
│   └── emotion_stability_analysis.png
│
├── case_studies/
│   ├── case_study_summary.csv
│   ├── test_027_lonely/
│   ├── test_054_scary/
│   └── ...
│
├── editor.py
├── emotion_mapper.py
├── emotion_editor.py
├── counterfactual.py
├── clip_evaluator.py
├── run_experiment.py
├── run_all_emotions.py
├── run_multi_images.py
├── analyze_multi_results.py
├── plot_multi_analysis.py
├── inspect_examples.py
├── export_case_images.py
├── summarize_case_studies.py
└── README.md
```

## 15. Main Modules

* `editor.py`: implements basic image editing operations, including brightness, contrast, saturation, and color temperature.
* `emotion_mapper.py`: maps each target emotion to a fixed editing preset.
* `emotion_editor.py`: applies the preset of a target emotion to an image.
* `counterfactual.py`: generates original, single-attribute, and all-attribute counterfactual image versions.
* `clip_evaluator.py`: loads CLIP and computes image-text similarity.
* `run_experiment.py`: runs one image and one emotion.
* `run_all_emotions.py`: runs all emotions on one image.
* `run_multi_images.py`: runs the full multi-image experiment.
* `analyze_multi_results.py`: computes average improvements and stability statistics.
* `plot_multi_analysis.py`: visualizes the final results.
* `inspect_examples.py`: finds top, bottom, and original-best cases.
* `export_case_images.py`: exports representative case study images.
* `summarize_case_studies.py`: summarizes selected case study scores.

## 16. Conclusion

This project demonstrates a small-scale CLIP-guided framework for analyzing affective image editing stability. The results suggest that fixed low-level visual edits work better for some emotions than others.

In particular, lonely and scary show stronger and more stable improvements, while happy and hopeful are more image-dependent and less reliably improved by fixed presets.

Rather than claiming to solve emotional image editing, this project provides an experimental framework for studying when simple visual edits are effective and when more adaptive or semantic methods may be needed.
