BOR-File
========

Small Python library to manipulate `BOR files`_

Installation
------------

Requirements:
  - python >= 3.8

You can install, upgrade, uninstall bor-file with these commands::

  $ pip install bor-file

To add support of exporting data to other formats (such as .zarr, .parquet or .xml)::

  $ pip install bor-file[extra]

Using a virtualenv may help overcome issues between python and your distribution.

Usage
-----

.. code-block:: python

  >>> import bor
  >>> bor_file = bor.read('./tests/data/parameters/DRILL/50000240718143044D/50000240718143044D.bor')


.. code-block:: python

  >>> bor_file.domain
  'DRILLING PARAMETERS'


.. code-block:: python

  >>> bor_file.description['borehole_ref']
  'TEST HOLE 1'

  >>> bor_file.description['drilling']['method']
  'DRLMTD_RTR'

BOR data can be used and edited as a `pandas DataFrame`_

.. code-block:: python

  >>> import pandas
  >>> pandas.set_option('display.precision', 2)
  >>>
  >>> bor_file.data
          DEPTH     AS  EVP  EVR     TP    IP     TQ   HP
  time
  0.0      7.71   0.00    0    0  53.20  0.00  41.60  0.0
  2.8      7.72  15.23    0    0  51.67  8.64  30.01  0.0
  4.0      7.73  33.78    0    0  51.67  5.90  32.45  0.0
  5.4      7.74  26.06    0    0  51.98  0.40  20.85  0.0
  8.0      7.75  14.03    0    0  51.98  0.00  20.85  0.0
  ...       ...    ...  ...  ...    ...   ...    ...  ...
  5211.2  19.95  16.58    0    0  55.34  8.03  33.06  0.1
  5214.0  19.96  13.03    0    0  55.03  0.10  25.12  0.1
  5219.4  19.97   6.76    0    0  55.34  0.00  33.97  0.1
  5224.4  19.98   7.30    0    0  54.42  0.10  28.17  0.1
  5233.8  20.00   7.30    0    0  55.34  0.00  35.19  0.0

  [1203 rows x 8 columns]

.. code-block:: python

  >>> bor_file.data.describe()
           DEPTH       AS     EVP       EVR       TP       IP       TQ       HP
  count  1203.00  1203.00  1203.0  1.20e+03  1203.00  1203.00  1203.00  1203.00
  mean     13.86    14.53     0.0  5.82e-03    53.30     5.30    31.07     0.05
  std       3.55    14.40     0.0  7.61e-02     1.53     7.83     7.54     0.09
  min       7.71     0.00     0.0  0.00e+00    47.40     0.00     8.03     0.00
  25%      10.78     9.12     0.0  0.00e+00    52.28     0.00    26.34     0.00
  50%      13.89    11.40     0.0  0.00e+00    53.81     0.71    30.31     0.00
  75%      16.94    15.20     0.0  0.00e+00    54.42     8.34    34.89     0.10
  max      20.00   182.43     0.0  1.00e+00    55.95    37.02    77.31     2.23

.. code-block:: python

  >>> bor_file.data.loc[:1]
        DEPTH   AS  EVP  EVR    TP   IP    TQ   HP
  time
  0.0    7.71  0.0    0    0  53.2  0.0  41.6  0.0

.. code-block:: python

  >>> bor_file.data.loc[0, 'DEPTH'] = 7
  >>> bor_file.data.loc[:1]
        DEPTH   AS  EVP  EVR    TP   IP    TQ   HP
  time
  0.0     7.0  0.0    0    0  53.2  0.0  41.6  0.0

.. code-block:: python

  >>> import matplotlib.pyplot as plt
  >>> bor_file.data.set_index('DEPTH').plot.area(figsize=(16, 6), y=['AS', 'TP'], subplots=True)

.. image:: docs/figure-example.png

You can export the data in any format supported by the pandas DataFrame class

.. code-block:: python

  >>> bor_file.to_csv('/tmp/data.csv')
  >>> bor_file.to_json('/tmp/data.json')
  >>> bor_file.to_zarr('/tmp/data.zarr', mode='w')  # need pip install bor-file[extra]
  >>> bor_file.to_xml('/tmp/data.xml')  # need pip install bor-file[extra]
  >>> bor_file.to_parquet('/tmp/data.parquet')  # need pip install bor-file[extra]

Changes can be made persistent with the `save` method..

.. code-block:: python

  >>> bor_file.save()

..or discarded with the `reset` method

.. code-block:: python

  >>> bor_file.reset()

.. _`pandas DataFrame`: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
.. _`BOR files`: https://bor-form.at/en/
