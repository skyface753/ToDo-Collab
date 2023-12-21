import 'package:client_flutter/src/constants/api.dart';
import 'package:client_flutter/src/core/data/error_data.dart';
import 'package:dio/dio.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
part 'user_repository.freezed.dart';
part 'user_repository.g.dart';

abstract class UserRepository {
  Future<dynamic> login(User req);
}

@freezed
class User with _$User {
  const factory User({
    required String name,
    required String password,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

class UserRepositoryImpl implements UserRepository {
  late Dio _dio;

  UserRepositoryImpl() {
    Uri baseUri = Uri(
        host: Api.host, port: Api.port, scheme: Api.schema, path: Api.basePath);
    _dio = Dio(
      BaseOptions(
        baseUrl: baseUri.toString(),
        responseType: ResponseType.json,
      ),
    );
  }

  static const String _loginPath = 'auth/login';
  static const String apiPrefix = 'api/v1';

  @override
  Future<dynamic> login(User request) async {
    try {
      final response = await _dio.post(_loginPath, data: request.toJson());
      Map<String, dynamic> user = response.data['user'];
      return User.fromJson(user);
    } on DioException catch (ex) {
      return ErrorResponse.fromJson(ex.response?.data);
    }
  }
}

final userRepositoryProvider = Provider<UserRepositoryImpl>((ref) {
  return UserRepositoryImpl();
});
