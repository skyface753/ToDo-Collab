import 'package:client_flutter/src/core/data/auth_repository.dart';
import 'package:client_flutter/src/core/data/error_data.dart';
import 'package:client_flutter/src/core/data/user_repository.dart';
import 'package:client_flutter/src/core/domain/user.dart';
import 'package:dartz/dartz.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

class UserController extends StateNotifier<AsyncValue<dynamic>> {
  UserController({
    required this.ref,
  }) : super(const AsyncData(null));
  Ref ref;

  Future<Either<String, bool>> login({
    required String username,
    required String password,
  }) async {
    state = const AsyncLoading();

    final User userReq = User(name: username, password: password);
    final response = await ref.read(userRepositoryProvider).login(userReq);
    if (response is ErrorResponse) {
      return Left(response.error.message);
    } else {
      await ref.read(authRepositoryProvider).setIsAuthenticated(username);
      return const Right(true);
    }
  }
}

final userControllerProvider =
    StateNotifierProvider<UserController, AsyncValue<dynamic>>((ref) {
  return UserController(ref: ref);
});
