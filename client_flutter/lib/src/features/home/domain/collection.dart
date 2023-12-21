import 'package:freezed_annotation/freezed_annotation.dart';
part 'collection.freezed.dart';
part 'collection.g.dart';

@freezed
abstract class Collection with _$Collection {
  const factory Collection({
    required String id,
    required String name,
    required List<Todo> todos,
  }) = _Collection;

  factory Collection.fromJson(Map<String, dynamic> json) =>
      _$CollectionFromJson(json);
}

@freezed
abstract class Todo with _$Todo {
  const factory Todo({
    required String id,
    required String title,
    required String description,
    @JsonKey(name: 'user_name') required String userName,
    @JsonKey(name: 'collection_id') required String collectionId,
  }) = _Todo;

  factory Todo.fromJson(Map<String, dynamic> json) => _$TodoFromJson(json);
}
