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
  >>> bor_file = bor.read('./tests/data/59650240611100849D.bor')


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

  >>> bor_file.data
                   DEPTH          AS    RV  EVP  EVR         TP         IP         TQ
  time
  0.000000      0.000000   76.099998   0.0  0.0  0.0   0.100000  21.100000   0.100000
  2.800000      0.020000   19.900000   0.0  0.0  0.0  24.500000  21.100000  14.700000
  3.000000      0.030000  278.899994   0.0  0.0  0.0  24.500000  21.100000  14.700000
  3.200000      0.050000  291.500000   0.0  0.0  0.0  24.500000  20.799999  14.700000
  3.400000      0.060000  253.500000   0.0  0.0  0.0  25.700001  20.600000  17.200001
  ...                ...         ...   ...  ...  ...        ...        ...        ...
  1220.599976  20.290001   47.500000  22.0  0.0  0.0  34.299999  20.600000  40.400002
  1221.599976  20.299999   38.000000  22.0  0.0  0.0  34.299999  20.600000  36.700001
  1222.599976  20.309999   40.599998  55.0  0.0  0.0  34.299999  21.100000  46.500000
  1223.800049  20.330000   95.099998  11.0  0.0  0.0  31.799999  17.299999  42.799999
  1224.599976  20.350000   93.000000   0.0  0.0  0.0  69.699997  16.500000  25.700001


.. code-block:: python

  >>> bor_file.data.describe()
               DEPTH           AS           RV     EVP     EVR           TP           IP           TQ
  count  1494.000000  1492.000000  1492.000000  1492.0  1492.0  1492.000000  1492.000000  1492.000000
  mean      9.929719   109.104691    41.548927     0.0     0.0    61.155632    19.434317    44.119774
  std       5.857386    79.709251    62.754272     0.0     0.0    14.612050     1.705973    10.935656
  min       0.030000     0.700000     0.000000     0.0     0.0     0.100000    12.200000     0.100000
  25%       4.942500    80.300003     8.000000     0.0     0.0    66.000000    19.700001    36.700001
  50%       9.755000   101.400002    31.000000     0.0     0.0    67.199997    20.000000    42.799999
  75%      14.617500   114.099998    59.000000     0.0     0.0    68.500000    20.200001    47.700001
  max      20.350000   735.200012  1653.000000     0.0     0.0    70.900002    21.799999   134.399994


.. code-block:: python

  >>> bor_file.data["DEPTH"] = bor_file.data["DEPTH"].round(2)

.. code-block:: python

  >>> bor_file.data.loc[:1]
        DEPTH         AS   RV  EVP  EVR   TP    IP   TQ
  time
  0.0     0.0  76.099998  0.0  0.0  0.0  0.1  21.1  0.1

.. code-block:: python

  >>> bor_file.data.loc[0, 'DEPTH'] = 0.01
  >>> bor_file.data.loc[:1]
        DEPTH         AS   RV  EVP  EVR   TP    IP   TQ
  time
  0.0    0.01  76.099998  0.0  0.0  0.0  0.1  21.1  0.1

.. code-block:: python

  >>> import matplotlib.pyplot as plt
  >>> bor_file.data.set_index('DEPTH').plot.area(figsize=(16, 6), y=['AS', 'TQ', 'TP'], subplots=True)

You can export the data in any format supported by the pandas DataFrame class

.. code-block:: python

  >>> bor_file.to_csv('/tmp/data.csv')
  >>> bor_file.to_json('/tmp/data.json')
  >>> bor_file.to_zarr('/tmp/data.zarr.zip', mode='w')  # need pip install bor-file[extra]
  >>> bor_file.to_xml('/tmp/data.xml')  # need pip install bor-file[extra]
  >>> bor_file.to_parquet('/tmp/data.parquet')  # need pip install bor-file[extra]

Changes can be made persistent with the `save` method..

.. code-block:: python

  >>> bor_file.save()

..or discarded with the `reset` method

  >>> bor_file.reset()

.. _`pandas DataFrame`: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
.. _`BOR files`: https://bor-form.at/en/
