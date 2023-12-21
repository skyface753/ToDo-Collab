// ignore_for_file: public_member_api_docs

import 'package:client_flutter/src/constants/api.dart';
import 'package:client_flutter/src/core/data/error_data.dart';
import 'package:client_flutter/src/utils/dio_provider.dart';
import 'package:client_flutter/src/utils/logger.dart';
import 'package:dio/dio.dart';
import 'package:freezed_annotation/freezed_annotation.dart';

import 'package:riverpod_annotation/riverpod_annotation.dart';
part 'user_repository.freezed.dart';
part 'user_repository.g.dart';

// abstract class UserRepository {
//   Future<dynamic> login(User req);
// }

@freezed
class User with _$User {
  const factory User({
    required String name,
    required String password,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

// class UserRepositoryImpl implements UserRepository {
//   late Dio _dio;

//   UserRepositoryImpl() {
//     Uri baseUri = Uri(
//     _dio = Dio(
//       BaseOptions(
//         baseUrl: baseUri.toString(),
//         responseType: ResponseType.json,
//       ),
//     );
//   }

//   static const String _loginPath = 'auth/login';
//   static const String apiPrefix = 'api/v1';

//   @override
//   Future<dynamic> login(User request) async {
//     try {
//       final response = await _dio.post(_loginPath, data: request.toJson());
//       Map<String, dynamic> user = response.data['user'];
//       return User.fromJson(user);
//     } on DioException catch (ex) {
//       return ErrorResponse.fromJson(ex.response?.data);
//     }
//   }
// }

// final userRepositoryProvider = Provider<UserRepositoryImpl>((ref) {
//   return UserRepositoryImpl();
// });

class UserRepository {
  UserRepository({required this.dio});
  final Dio dio;

  static const String _authPath = 'auth/login';

  String _getUrl({int? id}) {
    final url =
        Uri(scheme: Api.schema, host: Api.host, path: _authPath, port: Api.port)
            .toString();
    if (id != null) {
      return '$url$id';
    } else {
      return url;
    }
  }

  Future<dynamic> login(User request) async {
    try {
      final response = await dio.post<Map<String, dynamic>>(
        _getUrl(),
        data: request.toJson(),
      );
      logger.d('user_repository.login - response: $response');
      final userMap = response.data!['user'] as Map<String, dynamic>;

      return User.fromJson(userMap);
    } on DioException catch (ex) {
      return ErrorResponse.fromJson(ex.response?.data as Map<String, dynamic>);
    }
  }

  // Future<List<Collection>> getCollections() async {
  //   logger.d('collection_repository.getCollections');
  //   final url = _getUrl();
  //   final response = await dio.get<List<dynamic>>(url);
  //   if (response.statusCode == 200 && response.data != null) {
  //     final dataList = response.data!;
  //     return dataList
  //         .map(
  //           // (personJson) => Person.fromJson(personJson as Map<String, Object?>),
  //           (collectionJson) =>
  //               Collection.fromJson(collectionJson as Map<String, Object?>),
  //         )
  //         .toList();
  //   } else {
  //     throw ApiException(
  //       response.statusCode ?? -1,
  //       'getPeople ${response.statusCode}, data=${response.data}',
  //     );
  //   }
  // }
}

@riverpod
UserRepository userRepository(UserRepositoryRef ref) =>
    UserRepository(dio: ref.watch(dioProvider));

// @riverpod
// Future<List<Collection>> fetchCollections(FetchCollectionsRef ref) async {
//   logger.d('collection_repository.fetchCollections');
//   final repo = ref.read(userRepositoryProvider);
//   return repo.getCollections();
// }
