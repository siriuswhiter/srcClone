# srcClone
Clone Detection through srcClone: A Program Slicing Based Approach


# Install

1. [srcml](https://www.srcml.org/#download)
2. [srcslice - old version](http://www.sdml.cs.kent.edu/lmcrs/srcSlice/srcslice-ubuntu-14.04.tar.gz)
    > new version's srcslice still have wrong result.
3. python3 - `pip3 install numpy bitarray`

# Usage

```Python
python3 srcClone.py file_1 file_2
```

Quick test
```Python
python3 runtest.py 2>/dev/null
```

# Project Structure

```shell
srcClone
|-- srcClone.py     // main file 
|-- parse.py        // parse srcslice result to SliceProfile
|-- slice.py        // main function
|-- crANN.py        // crANN for Similarity matching
|-- lshash.py       // lshash
|-- storage.py      // storage for lshash
|-- runtest.py      // quick run testcase
`-- test            // testcase
```