import 'package:client_flutter/src/core/data/auth_repository.dart';
import 'package:cookie_jar/cookie_jar.dart';
import 'package:dio/dio.dart';
import 'package:dio_cookie_manager/dio_cookie_manager.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:pretty_dio_logger/pretty_dio_logger.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
// part 'dio_provider.g.dart';

// Interceptor when getting an unauthorized response
class UnauthorizedInterceptor extends Interceptor {
  UnauthorizedInterceptor(this.ref);
  final ProviderRef<Dio> ref;

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (err.response?.statusCode == 401) {
      print("Unauthorized Interceptor");
      ref.read(authRepositoryProvider).resetIsAuthenticated();
      // do something
    }
    super.onError(err, handler);
  }
}

final dioProvider = Provider<Dio>((ref) {
  final dio = Dio();
  dio.interceptors.add(
    PrettyDioLogger(
      requestHeader: true,
      responseBody: false,
      responseHeader: true,
    ),
  );
  dio.interceptors.add(
    CookieManager(
      PersistCookieJar(
        ignoreExpires: true,
      ),
    ),
  );
  dio.interceptors.add(
    UnauthorizedInterceptor(ref),
  );

  return dio;
});

// @riverpod
// Dio dio(DioRef ref) {
//   final dio = Dio();
//   dio.interceptors.add(
//     PrettyDioLogger(
//       requestHeader: true,
//       responseBody: false,
//       responseHeader: true,
//     ),
//   );
//   dio.interceptors.add(
//     CookieManager(
//       CookieJar(),
//     ),
//   );
//   return dio;
// }
