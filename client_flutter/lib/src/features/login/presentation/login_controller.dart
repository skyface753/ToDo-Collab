// import 'package:client_flutter/src/features/login/data/api_repository.dart';
// import 'package:flutter_riverpod/flutter_riverpod.dart';
// import 'package:go_router/go_router.dart';
// import 'package:riverpod_annotation/riverpod_annotation.dart';

// @riverpod
// class LoginController extends StateNotifier<LoginState> {
//   final ApiRepository apiRepository;
//   final GoRouter goRouter;

//   LoginController(this.apiRepository, this.goRouter) : super(LoginInitial());

//   // build
//   @override
//   FutureOr<LoginState> state = LoginInitial();

//   Future<void> login() async {
//     state = LoginLoading();
//     try {
//       final token = await apiRepository.login('username', 'password');
//       state = LoginSuccess(token);
//       goRouter.go('/home');
//     } catch (e) {
//       state = LoginError(e.toString());
//     }
//   }
// }

// abstract class LoginState {}

// class LoginInitial extends LoginState {}

// class LoginLoading extends LoginState {}

// class LoginSuccess extends LoginState {
//   final String token;

//   LoginSuccess(this.token);
// }

// class LoginError extends LoginState {
//   final String message;

//   LoginError(this.message);
// }
