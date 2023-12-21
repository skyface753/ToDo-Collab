import 'package:client_flutter/src/core/data/auth_repository.dart';
import 'package:client_flutter/src/core/data/error_data.dart';
import 'package:client_flutter/src/core/data/user_repository.dart';
import 'package:dartz/dartz.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

class UserController extends StateNotifier<AsyncValue<dynamic>> {
  Ref ref;

  UserController({
    required this.ref,
  }) : super(const AsyncData(null));

  Future<Either<String, bool>> login(
      {required String username, required String password}) async {
    state = const AsyncLoading();

    User userReq = User(name: username, password: password);
    final response = await ref.read(userRepositoryProvider).login(userReq);
    if (response is ErrorResponse) {
      return Left(response.error.message);
    } else {
      ref.read(setAuthStateProvider.notifier).state = response;
      ref.read(setIsAuthenticatedProvider(true));
      ref.read(setAuthenticatedUserProvider(response));
      return const Right(true);
    }
  }
}

final userControllerProvider =
    StateNotifierProvider<UserController, AsyncValue<dynamic>>((ref) {
  return UserController(ref: ref);
});
