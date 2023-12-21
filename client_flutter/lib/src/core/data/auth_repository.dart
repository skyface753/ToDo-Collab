import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:shared_preferences/shared_preferences.dart';

part 'auth_repository.g.dart';

class AuthRepository {
  AuthRepository(this.sharedPreferences);
  final SharedPreferences sharedPreferences;

  static const isAuthKey = 'isAuth';
  static const usernameKey = 'username';

  Future<void> setIsAuthenticated(String username) async {
    await sharedPreferences.setBool(isAuthKey, true);
    await sharedPreferences.setString(usernameKey, username);
  }

  Future<void> resetIsAuthenticated() async {
    await sharedPreferences.setBool(isAuthKey, false);
    await sharedPreferences.setString(usernameKey, '');
  }

  bool getIsAuthenticated() => sharedPreferences.getBool(isAuthKey) ?? false;

  // Future<void> setOnboardingComplete() async {
  //   await sharedPreferences.setBool(onboardingCompleteKey, true);
  // }

  // bool isOnboardingComplete() =>
  //     sharedPreferences.getBool(onboardingCompleteKey) ?? false;

  // Future<void> resetOnboarding() async {
  //   await sharedPreferences.setBool(onboardingCompleteKey, false);
  // }
}

/// The OnboardingRepository\
/// Use the `onboardingRepositoryProvider.overrideWithValue(localStorage)`\
/// to override the default value of the onboardingRepository\
/// See `main.dart` for an example
@Riverpod(keepAlive: true)
AuthRepository authRepository(AuthRepositoryRef ref) {
  throw UnimplementedError();
}


// // ignore: constant_identifier_names
// import 'dart:convert';

// import 'package:client_flutter/src/core/data/user_repository.dart';
// import 'package:hooks_riverpod/hooks_riverpod.dart';
// import 'package:shared_preferences/shared_preferences.dart';

// const isAuthenticatedKey = 'IS_AUTHENTICATED_KEY';
// const authenticatiedUsername = 'AUTHENTICATED_USER_NAME_KEY';

// final sharedPrefProvider = Provider((_) async {
//   return await SharedPreferences.getInstance();
// });

// final setAuthStateProvider = StateProvider<User?>(
//   (ref) => null,
// );

// final setIsAuthenticatedProvider = StateProvider.family<void, bool>(
//   (ref, isAuth) async {
//     final prefs = await ref.watch(sharedPrefProvider);
//     ref.watch(setAuthStateProvider);
//     prefs.setBool(
//       isAuthenticatedKey,
//       isAuth,
//     );
//   },
// );

// final setAuthenticatedUserProvider = StateProvider.family<void, User>(
//   (ref, userdata) async {
//     final prefs = await ref.watch(sharedPrefProvider);
//     ref.watch(setAuthStateProvider);
//     prefs.setString(
//       authenticatiedUsername,
//       json.encode(userdata),
//     );
//   },
// );

// final getIsAuthenticatedProvider = FutureProvider<bool>(
//   (ref) async {
//     final prefs = await ref.watch(sharedPrefProvider);
//     ref.watch(setAuthStateProvider);
//     return prefs.getBool(isAuthenticatedKey) ?? false;
//   },
// );

// final getAuthenticatedUserProvider = FutureProvider<User>(
//   (ref) async {
//     final prefs = await ref.watch(sharedPrefProvider);
//     ref.watch(setAuthStateProvider);
//     dynamic user = json.decode(prefs.getString(authenticatiedUsername) ?? "");
//     return User.fromJson(user);
//   },
// );

// // Todo: Handle logout or and reset
// final resetStorage = StateProvider<dynamic>(
//   (ref) async {
//     final prefs = await ref.watch(sharedPrefProvider);
//     final isCleared = await prefs.clear();
//     return isCleared;
//   },
// );
