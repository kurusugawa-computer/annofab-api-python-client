import shutil
import uuid
from pathlib import Path

import numpy
from PIL import Image

from annofabapi.segmentation import read_binary_image, write_binary_image

data_dir = Path("./tests/data/segmentation")
out_dir = Path("./tests/out/segmentation")


def setup_module(module):  # noqa: ARG001
    """
    `out_dir`配下に出力されるファイルが存在するかを確認するため、
    事前に`out_dir`配下のファイルを削除してゴミを残さないようにする。
    """
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(exist_ok=True, parents=True)


def test__read_binary_image():
    actual = read_binary_image(data_dir / "segment1")
    assert actual.shape == (64, 64)
    # ファイルオブジェクトでも読み込めるか確認
    with (data_dir / "segment1").open(mode="rb") as f:
        actual2 = read_binary_image(f)

    assert actual2.shape == (64, 64)


def test__write_binary_image():
    data = [[True, False], [False, False]]
    output_file = out_dir / str(uuid.uuid4())
    write_binary_image(data, output_file)
    assert output_file.exists()

    data2 = numpy.array(Image.open(output_file, formats=("PNG",)))
    assert data2.shape == (2, 2, 4)
    assert list(data2[0, 0]) == [255, 255, 255, 255]
    assert list(data2[0, 1]) == [0, 0, 0, 0]
