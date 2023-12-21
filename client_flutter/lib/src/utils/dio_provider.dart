import 'package:cookie_jar/cookie_jar.dart';
import 'package:dio/dio.dart';
import 'package:dio_cookie_manager/dio_cookie_manager.dart';
import 'package:pretty_dio_logger/pretty_dio_logger.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
// part 'dio_provider.g.dart';

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
