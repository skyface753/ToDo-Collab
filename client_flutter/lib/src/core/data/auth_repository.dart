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
}

/// The OnboardingRepository\
/// Use the `onboardingRepositoryProvider.overrideWithValue(localStorage)`\
/// to override the default value of the onboardingRepository\
/// See `main.dart` for an example
@Riverpod(keepAlive: true)
AuthRepository authRepository(AuthRepositoryRef ref) {
  throw UnimplementedError();
}
