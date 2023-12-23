// ignore_for_file: public_member_api_docs

import 'package:client_flutter/src/constants/api.dart';
import 'package:client_flutter/src/exceptions/api_exception.dart';
import 'package:client_flutter/src/features/home/domain/collection.dart';
import 'package:client_flutter/src/utils/dio_provider.dart';
import 'package:client_flutter/src/utils/logger.dart';
import 'package:dio/dio.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'collection_repository.g.dart';

class CollectionRepository {
  CollectionRepository({required this.dio});
  final Dio dio;

  static const String apiPrefix = 'api/v1';
  static const String _collectionPath = '$apiPrefix/collection';

  String _getCollectionUrl({String? id}) {
    final url = Uri(
      scheme: Api.schema,
      host: Api.host,
      path: _collectionPath,
      port: Api.port,
    ).toString();
    if (id != null) {
      return '$url/$id';
    } else {
      return url;
    }
  }

  Future<List<Collection>> getCollections() async {
    logger.d('collection_repository.getCollections');
    try {
      final response = await dio.get<List<dynamic>>(_getCollectionUrl());
      logger.d('response: $response');
      if (response.statusCode == 200 && response.data != null) {
        final dataList = response.data!;
        return dataList
            .map<Collection>(
              (json) => Collection.fromJson(json as Map<String, dynamic>),
            )
            .toList();
      } else {
        // return [];
        throw ApiException(
          response.statusCode ?? -1,
          'getCollections ${response.statusCode}, data=${response.data}',
        );
      }
    } catch (e) {
      logger.e('collection_repository.getCollections: $e');
      // rethrow;
      // return [];
      throw ApiException(-1, 'getCollections $e');
    }
  }

  Future<Collection> getCollection(String collectionId) async {
    logger.d('collection_repository.getCollection');
    try {
      final response = await dio.get<Map<String, dynamic>>(
        _getCollectionUrl(id: collectionId),
        queryParameters: {'generate_websocket_url': true},
      );
      logger.d('response: $response');
      if (response.statusCode == 200 && response.data != null) {
        return Collection.fromJson(response.data!);
      } else {
        throw ApiException(
          response.statusCode ?? -1,
          'getCollection ${response.statusCode}, data=${response.data}',
        );
      }
    } catch (e) {
      logger.e('collection_repository.getCollection: $e');
      throw ApiException(-1, 'getCollection $e');
    }
  }

  Future<Collection> createCollection(String name) async {
    logger.d('collection_repository.createCollection');
    try {
      final response = await dio.post<Map<String, dynamic>>(
        _getCollectionUrl(),
        data: {'name': name},
      );
      logger.d('response: $response');
      if (response.statusCode == 201 && response.data != null) {
        return Collection.fromJson(response.data!);
      } else {
        throw ApiException(
          response.statusCode ?? -1,
          'createCollection ${response.statusCode}, data=${response.data}',
        );
      }
    } catch (e) {
      logger.e('collection_repository.createCollection: $e');
      throw ApiException(-1, 'createCollection $e');
    }
  }
}

@riverpod
CollectionRepository collectionRepository(CollectionRepositoryRef ref) =>
    CollectionRepository(
      dio: ref.watch(dioProvider),
    );

@riverpod
Future<List<Collection>> fetchCollections(
  FetchCollectionsRef ref,
) {
  logger.d('collection_repository.fetchCollections');
  final repo = ref.read(collectionRepositoryProvider);
  return repo.getCollections();
}

@riverpod
Future<Collection> fetchCollection(
  FetchCollectionRef ref,
  String collectionId,
) async {
  logger.d('collection_repository.fetchCollection');
  final repo = ref.read(collectionRepositoryProvider);
  return repo.getCollection(collectionId);
}
