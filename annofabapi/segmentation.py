import numpy
import numpy.typing as npt
from PIL import Image


def read_binary_image(fp) -> numpy.ndarray:
    """
    アノテーションZIP(ディレクトリ)に格納されている塗りつぶし画像を読み込みます。

    Args:
        fp: A filename (string), pathlib.Path object or file object.

    Returns:
        numpyの2次元配列。`dtype`はbool。
        各要素の値は、塗られている部分([255,255,255,255])はTrue, 塗られていない部分([0,0,0,0])はFalseです。
    """
    image = Image.open(fp, formats=("PNG",)).convert("1")
    return numpy.array(image, dtype=bool)


def write_binary_image(array: npt.ArrayLike, fp) -> None:
    """
    booleanの2次元配列から、Annofab用の塗りつぶし画像を書き出します。

    Args:
        array: 2次元配列。各要素はboolean。
            Trueは[255,255,255,255], Falseは[0,0,0,0]で塗りつぶされます。
        fp: A filename (string), pathlib.Path object or file object.

    """
    mask_array = numpy.array(array, dtype=bool)
    height, width = mask_array.shape
    channel = 4  # RGBAの4チャンネル
    data = numpy.zeros((height, width, channel), dtype=numpy.uint8)
    data[mask_array] = [255, 255, 255, 255]
    Image.fromarray(data, mode="RGBA").save(fp, format="PNG")
