from pathlib import Path

from counterfactual import save_counterfactual_edits


cases = [
    ("test_027", "lonely"),
    ("test_023", "lonely"),
    ("test_023", "scary"),
    ("test_054", "scary"),
    ("test_085", "romantic"),
    ("test_041", "hopeful"),
    ("test_029", "hopeful"),
]


input_dir = Path("images/multi")
output_root = Path("case_studies")

output_root.mkdir(exist_ok=True)


def main():
    for image_name, emotion in cases:
        input_path = input_dir / f"{image_name}.jpg"
        output_dir = output_root / f"{image_name}_{emotion}"

        output_dir.mkdir(exist_ok=True)

        print("=" * 60)
        print(f"Exporting case: {image_name}, emotion: {emotion}")
        print(f"Input: {input_path}")
        print(f"Output: {output_dir}")

        save_counterfactual_edits(
            input_path=str(input_path),
            emotion=emotion,
            output_dir=str(output_dir),
        )

    print("=" * 60)
    print("Case images exported.")


if __name__ == "__main__":
    main()