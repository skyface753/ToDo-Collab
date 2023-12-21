import 'package:client_flutter/src/exceptions/api_exception.dart';
import 'package:client_flutter/src/features/home/domain/collection.dart';
import 'package:dio/dio.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../../constants/api.dart';
import '../../../utils/dio_provider.dart';
import '../../../utils/logger.dart';
part 'collection_repository.g.dart';

class CollectionRepository {
  CollectionRepository(
      // {required this.dio}
      );
  // final Dio dio;

  static const String apiPrefix = 'api/v1';
  static const String _collectionPath = '$apiPrefix/collection';

  String _getCollectionUrl({int? id}) {
    final url = Uri(
            scheme: Api.schema,
            host: Api.host,
            path: _collectionPath,
            port: Api.port)
        .toString();
    if (id != null) {
      return '$url$id';
    } else {
      return url;
    }
  }

  Future<List<Collection>> getCollections(WidgetRef ref) async {
    logger.d('collection_repository.getCollections');
    final dio = ref.watch(dioProvider);
    final response = await dio.get(_getCollectionUrl());
    logger.d('response: $response');
    if (response.statusCode == 200 && response.data != null) {
      final dataList = response.data!;
      return dataList
          .map<Collection>((json) => Collection.fromJson(json))
          .toList();
    } else {
      throw ApiException(
        response.statusCode ?? -1,
        'getPeople ${response.statusCode}, data=${response.data}',
      );
    }
  }
}

@riverpod
CollectionRepository collectionRepository(CollectionRepositoryRef ref) =>
    CollectionRepository();

@riverpod
Future<List<Collection>> fetchCollections(
    FetchCollectionsRef ref, WidgetRef ref2) {
  logger.d('collection_repository.fetchCollections');
  final repo = ref.read(collectionRepositoryProvider);
  return repo.getCollections(ref2);
}
