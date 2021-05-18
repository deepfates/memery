# memery
> Search over large image datasets with computer vision!


## Install

`pip install memery`

## How to use

Simply use queryFlow to search over a folder recursively!

```python
ranked = queryFlow('./images', 'a funny dog meme')
```

    Searching 78 images


```python
printi(ranked)
```


![jpeg](output_5_0.jpg)



![jpeg](output_5_1.jpg)



![jpeg](output_5_2.jpg)


## TODO:

- Interactive GUI
- Optimize the image loader and number of trees based on memory and db size
- Type annotations

## DONE:
- _Code for joining archived data to new data_
- _Code for saving indexes to archive_
- _Flows_
- _Cleanup repo_

