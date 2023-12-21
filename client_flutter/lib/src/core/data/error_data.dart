import 'package:freezed_annotation/freezed_annotation.dart';
part 'error_data.freezed.dart';
part 'error_data.g.dart';

@freezed
class ErrorResponse with _$ErrorResponse {
  const factory ErrorResponse({
    dynamic data,
    required Error error,
  }) = _ErrorResponse;

  factory ErrorResponse.fromJson(Map<String, dynamic> json) =>
      _$ErrorResponseFromJson(json);
}

@freezed
class Error with _$Error {
  const factory Error({
    required int status,
    required String name,
    required String message,
    required Details details,
  }) = _Error;

  factory Error.fromJson(Map<String, dynamic> json) => _$ErrorFromJson(json);
}

@freezed
class Details with _$Details {
  const factory Details() = _Details;

  factory Details.fromJson(Map<String, dynamic> json) =>
      _$DetailsFromJson(json);
}
