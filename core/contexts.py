import time
import contextlib

from maya import cmds


@contextlib.contextmanager
def undo_chunk_context(undo_chunk_name=None):
	if undo_chunk_name is None:
		cmds.undoInfo(openChunk=True)
	else:
		cmds.undoInfo(openChunk=True, chunkName=undo_chunk_name)

	yield

	if undo_chunk_name is None:
		cmds.undoInfo(closeChunk=True)
	else:
		cmds.undoInfo(closeChunk=True, chunkName=undo_chunk_name)


@contextlib.contextmanager
def undo_after_context(undo_chunk_name=None):

	with undo_chunk_context(undo_chunk_name=undo_chunk_name):
		yield

	cmds.undo()


@contextlib.contextmanager
def time_it_context(name):
	print(f'\n[time_it_context] - {name}')

	start_timer = time.time()

	yield

	end_timer = time.time()
	print(f'[{name}] - Took {end_timer - start_timer:.3f} seconds')
