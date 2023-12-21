// import 'dart:convert';

// import 'package:client_flutter/src/constants/api.dart';
// import 'package:client_flutter/src/utils/dio_provider.dart';
// import 'package:dio/dio.dart';
// import 'package:riverpod_annotation/riverpod_annotation.dart';

// part 'api_repository.g.dart';

// class ApiRepository {
//   final Dio dio;

//   ApiRepository(this.dio);

//   String _getUrl({int? id, String? path}) {
//     final url = Uri(
//       scheme: Api.schema,
//       host: Api.host,
//       path: Api.basePath + (path ?? ''),
//       port: Api.port,
//     ).toString();
//     if (id != null) {
//       return '$url$id';
//     } else {
//       return url;
//     }
//   }

//   Future<String> login(String username, String password) async {
//     final response = await dio.post(
//       _getUrl(path: 'login'),
//       data: jsonEncode({
//         'username': username,
//         'password': password,
//       }),
//     );
//     return response.data['access_token'];
//   }
// }

// @riverpod
// ApiRepository apiRepository(DioRef ref) {
//   return ApiRepository(ref.read(dioProvider));
// }
