import 'package:client_flutter/src/core/data/auth_repository.dart';
import 'package:client_flutter/src/features/home_screen.dart';
import 'package:client_flutter/src/features/login/presentation/login_screen.dart';
import 'package:client_flutter/src/utils/logger.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

// import '../features/login/presentation/login_screen.dart';
// import '../features/rest_crud_demo/domain/person.dart';
// import '../features/rest_crud_demo/presentation/details_screen.dart';
// import '../features/rest_crud_demo/presentation/home_screen.dart';
import 'scaffold_with_navigation.dart';

part 'app_router.g.dart';

// general ideas on navigation see https://m2.material.io/design/navigation/understanding-navigation.html#forward-navigation

// shell routes, appear in the bottom navigation
// see https://pub.dev/documentation/go_router/latest/go_router/ShellRoute-class.html
enum TopLevelDestinations { home, login, loading }

// GlobalKey is a factory, hence each call creates a key
//this is root, even if it navigates to home, it needs a separate key!!!
final _rootNavigatorKey = GlobalKey<NavigatorState>();
final _homeNavigatorKey =
    GlobalKey<NavigatorState>(debugLabel: TopLevelDestinations.home.name);
final _loginNavigatorKey =
    GlobalKey<NavigatorState>(debugLabel: TopLevelDestinations.login.name);
final _loadingNavigatorKey =
    GlobalKey<NavigatorState>(debugLabel: TopLevelDestinations.loading.name);

// other destinations, reachable from a top level destination
// enum SubRoutes { details }

// enum Parameter { id }

//https://github.com/flutter/packages/blob/main/packages/go_router/example/lib/stateful_shell_route.dart

@Riverpod(keepAlive: true)
GoRouter goRouter(GoRouterRef ref) {
  final authRepository = ref.watch(authRepositoryProvider);
  return GoRouter(
    initialLocation: '/${TopLevelDestinations.home.name}',
    navigatorKey: _rootNavigatorKey,
    debugLogDiagnostics: true,
    redirect: (context, state) {
      final isAuth = authRepository.getIsAuthenticated();
      logger.d('isAuthenticated: ${isAuth}');
      if (!isAuth) {
        return '/${TopLevelDestinations.login.name}';
      }
      return null;
      // if (authRepository.value!) {
      //   // return '/${TopLevelDestinations.home.name}';
      //   return null;
      // } else {
      //   return '/${TopLevelDestinations.login.name}';
      // }
    },
    routes: [
      // Stateful navigation based on:
      // https://github.com/flutter/packages/blob/main/packages/go_router/example/lib/stateful_shell_route.dart
      StatefulShellRoute.indexedStack(
        builder: (context, state, navigationShell) {
          return ScaffoldWithNavigation(navigationShell: navigationShell);
        },
        branches: [
          StatefulShellBranch(
            navigatorKey: _homeNavigatorKey,
            routes: [
              // base route home
              GoRoute(
                path: '/${TopLevelDestinations.home.name}', // path: /home
                name: TopLevelDestinations.home.name,
                pageBuilder: (context, state) => NoTransitionPage(
                  key: state.pageKey,
                  child: HomeScreen(),
                ),
                // routes: <RouteBase>[
                //   // The details screen to display stacked on navigator of the
                //   // first tab. This will cover screen A but not the application
                //   // shell (bottom navigation bar).
                //   GoRoute(
                //     path: '${SubRoutes.details.name}/:${Parameter.id.name}',
                //     name: SubRoutes.details.name,
                //     builder: (BuildContext context, GoRouterState state) {
                //       // alternatively use https://pub.dev/documentation/go_router/latest/topics/Type-safe%20routes-topic.html
                //       final id =
                //           int.parse(state.pathParameters[Parameter.id.name]!);
                //       final person = _extractPersonFromExtra(state.extra);
                //       return DetailsScreen(id: id, person: person);
                //     },
                //   ),
                // ],
              ),
            ],
          ),
          StatefulShellBranch(
            navigatorKey: _loginNavigatorKey,
            routes: [
              GoRoute(
                path: '/${TopLevelDestinations.login.name}',
                name: TopLevelDestinations.login.name,
                pageBuilder: (context, state) => NoTransitionPage(
                  key: state.pageKey,
                  child: const LoginScreen(),
                ),
              ),
            ],
          ),
        ],
      ),
      // Loading screen
      GoRoute(
        path: '/${TopLevelDestinations.loading.name}',
        name: TopLevelDestinations.loading.name,
        pageBuilder: (context, state) => NoTransitionPage(
          key: state.pageKey,
          child: const LoginScreen(),
        ),
      ),
    ],
  );
}
