from skimage import img_as_float
import numpy as np


def align(img, g_coord):
    """
    Сопоставляет изображения с фотографий Прокудина-Горского и
    возвращает координаты точек на синем и красном каналах
    координаты точки на зеленом канале
    Вход: ссылка на изображение, координаты точки на зеленом канале.
    Выход: координаты точек на синем и красном каналах.
    """

    row_g, col_g = g_coord

    img_f = img_as_float(img) if img.dtype != "float64" else img

    vertical_border = int(img_f.shape[1] * 0.12 // 2)  # вертикальная рамка
    one_third_rows = img_f.shape[0] // 3  # высота одного изображения
    # горизонтальная рамка
    horizontal_border = int((img_f.shape[0] // 3) * 0.07)

    (b, g, r) = [
        img_f[
            one_third_rows * i
            + horizontal_border : one_third_rows * (i + 1)
            - horizontal_border,
            vertical_border:-(vertical_border),
        ]
        for i in range(3)
    ]

    max_correlation_params = {
        0: {
            "image": "blue channel",
            "max_arr": np.array([]),
            "max_correlation": 0,
            "max_row": -15,
            "max_column": -15,
        },
        1: {
            "image": "red channel",
            "max_arr": np.array([]),
            "max_correlation": 0,
            "max_row": -15,
            "max_column": -15,
        },
    }

    for img_channel in enumerate((b, r)):
        for row_shift in range(-15, 16):
            # циклический сдвиг - 0 строки, 1 столбцы
            arr_rolled_row = np.roll(img_channel[1], row_shift, axis=0)
            for column_shift in range(-15, 16):
                # циклический сдвиг - 0 строки, 1 столбцы
                arr_rolled = np.roll(arr_rolled_row, column_shift, axis=1)
                correlation = (arr_rolled * g).sum()

                if (
                    correlation
                    > max_correlation_params[img_channel[0]]["max_correlation"]
                ):
                    max_correlation_params[img_channel[0]]["max_row"] = row_shift
                    max_correlation_params[img_channel[0]]["max_column"] = column_shift
                    max_correlation_params[img_channel[0]][
                        "max_correlation"
                    ] = correlation
                    max_correlation_params[img_channel[0]]["max_arr"] = arr_rolled

    (row_b, col_b) = (
        row_g - (img.shape[0] // 3) - max_correlation_params[0]["max_row"],
        col_g - max_correlation_params[0]["max_column"],
    )
    (row_r, col_r) = (
        row_g + (img.shape[0] // 3) - max_correlation_params[1]["max_row"],
        col_g - max_correlation_params[1]["max_column"],
    )
    return (row_b, col_b), (row_r, col_r)
