// ignore_for_file: public_member_api_docs

import 'package:client_flutter/src/constants/api.dart';
import 'package:client_flutter/src/core/data/error_data.dart';
import 'package:client_flutter/src/core/domain/user.dart';
import 'package:client_flutter/src/utils/dio_provider.dart';
import 'package:client_flutter/src/utils/logger.dart';
import 'package:dio/dio.dart';

import 'package:riverpod_annotation/riverpod_annotation.dart';
part 'user_repository.g.dart';

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
      if (response.statusCode == 200) {
        final userMap = response.data!['user'] as Map<String, dynamic>;
        return User.fromJson(userMap);
      } else {
        return ErrorResponse.fromJson(response.data as Map<String, dynamic>);
      }
    } on DioException catch (ex) {
      return ErrorResponse.fromJson(ex.response?.data as Map<String, dynamic>);
    }
  }
}

@riverpod
UserRepository userRepository(UserRepositoryRef ref) =>
    UserRepository(dio: ref.watch(dioProvider));
