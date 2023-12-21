// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'error_data.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$ErrorResponseImpl _$$ErrorResponseImplFromJson(Map<String, dynamic> json) =>
    _$ErrorResponseImpl(
      error: Error.fromJson(json['error'] as Map<String, dynamic>),
      data: json['data'],
    );

Map<String, dynamic> _$$ErrorResponseImplToJson(_$ErrorResponseImpl instance) =>
    <String, dynamic>{
      'error': instance.error,
      'data': instance.data,
    };

_$ErrorImpl _$$ErrorImplFromJson(Map<String, dynamic> json) => _$ErrorImpl(
      status: json['status'] as int,
      name: json['name'] as String,
      message: json['message'] as String,
      details: Details.fromJson(json['details'] as Map<String, dynamic>),
    );

Map<String, dynamic> _$$ErrorImplToJson(_$ErrorImpl instance) =>
    <String, dynamic>{
      'status': instance.status,
      'name': instance.name,
      'message': instance.message,
      'details': instance.details,
    };

_$DetailsImpl _$$DetailsImplFromJson(Map<String, dynamic> json) =>
    _$DetailsImpl();

Map<String, dynamic> _$$DetailsImplToJson(_$DetailsImpl instance) =>
    <String, dynamic>{};
