```python

Traceback (most recent call last):
  File "/home/pokorie/Documents/repos/mimic/src/ml/runner/predictor_manager.py", line 152, in predict
    return self.current_runner.predict(x)[0]
  File "/home/pokorie/Documents/repos/mimic/src/ml/runner/mab/mab_runner.py", line 77, in predict
    return model.predict(x)
  File "/home/pokorie/Documents/repos/mimic/src/venv/lib/python3.8/site-packages/contextualbandits/online.py", line 708, in predict
    pred[ix_change_rnd] = np.random.randint(self.nchoices, size = ix_change_rnd.sum())
IndexError: boolean index did not match indexed array along dimension 0; dimension is 1 but corresponding boolean dimension is 8

```