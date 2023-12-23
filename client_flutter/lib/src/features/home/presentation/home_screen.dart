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
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          CreateCollectionOverlay(
            context: context,
            ref: ref,
          ).show();
        },
        child: const Icon(Icons.add),
      ),
      body: isAuth
          ? RefreshIndicator(
              onRefresh: () async {
                ref.invalidate(fetchCollectionsProvider);
              },
              child:
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
                        },
                      );
                    },
                  );
                },
              ),
            )
          : const Text('Not Authenticated'),
    );
  }
}

class CreateCollectionOverlay {
  CreateCollectionOverlay({
    required this.context,
    required this.ref,
  });

  final BuildContext context;
  final WidgetRef ref;
  final TextEditingController _nameController = TextEditingController();

  Future<void> show() async {
    return showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Create Collection'),
          content: TextField(
            controller: _nameController,
            decoration: const InputDecoration(
              labelText: 'Name',
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () async {
                final name = _nameController.text;
                if (name.isNotEmpty) {
                  try {
                    await ref
                        .read(collectionRepositoryProvider)
                        .createCollection(name);
                    ref.invalidate(fetchCollectionsProvider);
                    // ignore: use_build_context_synchronously
                    Navigator.of(context).pop();
                  } catch (e) {
                    // ignore: use_build_context_synchronously
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text(e.toString()),
                      ),
                    );
                  }
                }
              },
              child: const Text('Create'),
            ),
          ],
        );
      },
    );
  }
}
