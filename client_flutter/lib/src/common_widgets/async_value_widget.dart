// ignore_for_file: public_member_api_docs

import 'package:client_flutter/src/exceptions/api_exception.dart';
import 'package:client_flutter/src/utils/localization.dart';
import 'package:client_flutter/src/utils/logger.dart';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

//credits to  Code with Andrea https://github.com/bizz84/starter_architecture_flutter_firebase/blob/master/lib/src/common_widgets/async_value_widget.dart
class AsyncValueWidget<T> extends StatelessWidget {
  const AsyncValueWidget({required this.value, required this.data, super.key});
  final AsyncValue<T> value;
  final Widget Function(T) data;

  @override
  Widget build(BuildContext context) {
    return value.when(
      data: data,
      error: (error, st) => Center(child: ErrorMessageWidget(error)),
      loading: () => const SizedBox(
        width: 60,
        height: 60,
        child: Center(child: CircularProgressIndicator()),
      ),
    );
  }
}

//credits to Code with Andrea https://github.com/bizz84/starter_architecture_flutter_firebase/blob/master/lib/src/common_widgets/error_message_widget.dart

/// Simple reusable widget to show errors to the user.
class ErrorMessageWidget extends StatelessWidget {
  const ErrorMessageWidget(this.error, {super.key});

  /// Error object, might be a DioException.
  final Object? error;
  @override
  Widget build(BuildContext context) {
    return Text(
      _pimpError(error, context.loc.error),
      style:
          Theme.of(context).textTheme.titleLarge!.copyWith(color: Colors.red),
    );
  }

  String _pimpError(Object? error, String defaultStr) {
    if (error == null) {
      logger.d('ErrorMessageWidget - _pimpError - no error');
      return defaultStr;
    }
    try {
      final dioEx = error as DioException;
      if (dioEx.response != null) {
        final map = dioEx.response!.data as Map<String, dynamic>;
        if (map.containsKey('detail')) {
          return map['detail']! as String;
        }
      }
    } catch (ex) {
      logger.e(
        'ErrorMessageWidget - _pimpError - could not extract info',
        error: ex,
      );
    }
    try {
      final apiException = error as ApiException;
      return 'status ${apiException.statusCode}: ${apiException.message}';
    } catch (ex) {
      logger.e(
        'ErrorMessageWidget - _pimpError - could not extract message',
        error: ex,
      );
    }
    return defaultStr;
  }
}
