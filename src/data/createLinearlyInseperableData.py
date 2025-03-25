from collections import defaultdict
from pathlib import Path
from typing import List

import click
import matplotlib.pyplot as plt
import pandas
from pandas import DataFrame


def createIncreasingData(
    xMin: int,
    xMax: int,
    a: int,
    _class: int = 0,
) -> DataFrame:
    """
    Create data from the following formula:

    `y = x + a`

    Where `x` is a value from [xMin, xMax] and `a` is a constant.
    `_class` is an integer label for the (x, y) pairing.
    """

    data: dict[str, List[int]] = defaultdict(list)

    x: int
    for x in range(xMin, xMax, 1):
        data["x"].append(x)
        data["y"].append(x + a)
        data["class"].append(_class)

    return DataFrame(data=data)


def createDecreasingData(
    xMin: int,
    xMax: int,
    a: int,
    _class: int = 1,
) -> DataFrame:
    """
    Create data from the following formula:

    `y = a - x`

    Where `x` is a value from [xMin, xMax] and `a` is a constant.
    `_class` is an integer label for the (x, y) pairing.
    """

    data: dict[str, List[int]] = defaultdict(list)

    x: int
    for x in range(xMin, xMax, 1):
        data["x"].append(x)
        data["y"].append(a - x)
        data["class"].append(_class)

    return DataFrame(data=data)


def plotData(df1: DataFrame, df2: DataFrame, fp: Path) -> None:
    """
    Plot two DataFrames on the same figure and save to a file
    """

    plt.scatter(x=df1["x"], y=df1["y"], marker="x")
    plt.scatter(x=df2["x"], y=df2["y"], marker="o")

    plt.title(label="Linearly Inseperable Data Example")
    plt.xlabel(xlabel="X Values")
    plt.ylabel(ylabel="Y Values")

    plt.savefig(fp)


@click.command()
@click.option(
    "--fig",
    "figOutput",
    help="Path to store figure",
    type=click.Path(
        exists=False,
        file_okay=True,
        writable=True,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
)
@click.option(
    "--data",
    "dataOutput",
    help="Path to store data in CSV format",
    type=click.Path(
        exists=False,
        file_okay=True,
        writable=True,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
)
@click.option(
    "--samples",
    "samples",
    help="Number of samples to generate",
    type=int,
    default=50,
    required=False,
    show_default=True,
)
def main(figOutput: Path, dataOutput: Path, samples: int) -> None:
    df1: DataFrame = createDecreasingData(xMin=0, xMax=samples, a=samples)
    df2: DataFrame = createIncreasingData(xMin=0, xMax=samples, a=1)

    plotData(df1=df1, df2=df2, fp=figOutput)

    pandas.concat(objs=[df1, df2]).to_csv(path_or_buf=dataOutput, index=False)


if __name__ == "__main__":
    main()
