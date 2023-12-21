// ignore: constant_identifier_names
import 'dart:convert';

import 'package:client_flutter/src/core/data/user_repository.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

const isAuthenticatedKey = 'IS_AUTHENTICATED_KEY';
const authenticatiedUsername = 'AUTHENTICATED_USER_NAME_KEY';

final sharedPrefProvider = Provider((_) async {
  return await SharedPreferences.getInstance();
});

final setAuthStateProvider = StateProvider<User?>(
  (ref) => null,
);

final setIsAuthenticatedProvider = StateProvider.family<void, bool>(
  (ref, isAuth) async {
    final prefs = await ref.watch(sharedPrefProvider);
    ref.watch(setAuthStateProvider);
    prefs.setBool(
      isAuthenticatedKey,
      isAuth,
    );
  },
);

final setAuthenticatedUserProvider = StateProvider.family<void, User>(
  (ref, userdata) async {
    final prefs = await ref.watch(sharedPrefProvider);
    ref.watch(setAuthStateProvider);
    prefs.setString(
      authenticatiedUsername,
      json.encode(userdata),
    );
  },
);

final getIsAuthenticatedProvider = FutureProvider<bool>(
  (ref) async {
    final prefs = await ref.watch(sharedPrefProvider);
    ref.watch(setAuthStateProvider);
    return prefs.getBool(isAuthenticatedKey) ?? false;
  },
);

final getAuthenticatedUserProvider = FutureProvider<User>(
  (ref) async {
    final prefs = await ref.watch(sharedPrefProvider);
    ref.watch(setAuthStateProvider);
    dynamic user = json.decode(prefs.getString(authenticatiedUsername) ?? "");
    return User.fromJson(user);
  },
);

// Todo: Handle logout or and reset
final resetStorage = StateProvider<dynamic>(
  (ref) async {
    final prefs = await ref.watch(sharedPrefProvider);
    final isCleared = await prefs.clear();
    return isCleared;
  },
);
