import 'package:client_flutter/src/common_widgets/async_value_widget.dart';
import 'package:client_flutter/src/core/data/auth_repository.dart';
import 'package:client_flutter/src/features/home/data/collection_repository.dart';
import 'package:client_flutter/src/routing/app_router.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isAuth = ref.watch(authRepositoryProvider).getIsAuthenticated();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Home Screen'),
      ),
      body: isAuth
          ?
          // Text("HI")
          AsyncValueWidget(
              value: ref.watch(fetchCollectionsProvider),
              data: (data) {
                return ListView.builder(
                  itemCount: data.length,
                  itemBuilder: (context, index) {
                    return ListTile(
                        title: Text(data[index].id),
                        subtitle: Text(data[index].name),
                        onTap: () {
                          context.goNamed(
                            CollectionSubRoutes.collection.name,
                            pathParameters: {
                              Parameter.id.name: data[index].id,
                            },
                          );
                        });
                  },
                );
              },
            )
          : const Text('Not Authenticated'),
    );
  }
}
