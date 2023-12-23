import 'package:client_flutter/src/features/home/data/collection_repository.dart';
import 'package:client_flutter/src/features/home/domain/collection.dart';
import 'package:client_flutter/src/utils/logger.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
part 'collection_controller.g.dart';

@riverpod
class CollectionController extends _$CollectionController {
  @override
  FutureOr<Collection?> build() {
    ref.onDispose(
      () => logger.i('CollectionController ----- dispose controller -----'),
    );
    state = const AsyncData(null);
    return state.value;
  }

  Future<void> getCollection(String collectionId) async {
    logger.d('collection_controller.getCollection');
    try {
      final collectionRepo = ref.read(collectionRepositoryProvider);
      final collection = await collectionRepo.getCollection(collectionId);
      state = AsyncData(collection);
    } catch (e) {
      logger.e('collection_controller.getCollection: $e');
      state = AsyncError(e, StackTrace.current);
    }
  }

  // Just add it to the collection, not to the server (for the websocket)
  Future<void> addTodoToCollectionTodos(Todo todo) async {
    logger.d('collection_controller.addTodoToCollectionTodos');
    try {
      final collection = state.value;
      if (collection != null) {
        final newCollection = collection.copyWith(
          todos: [...collection.todos ?? [], todo],
        );
        state = AsyncData(newCollection);
      }
    } catch (e) {
      logger.e('collection_controller.addTodoToCollectionTodos: $e');
      state = AsyncError(e, StackTrace.current);
    }
  }
}
