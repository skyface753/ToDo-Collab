import 'package:client_flutter/src/common_widgets/async_value_widget.dart';
import 'package:client_flutter/src/core/data/auth_repository.dart';
import 'package:client_flutter/src/features/home/data/collection_repository.dart';
import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

class HomeScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isAuth = ref.watch(authRepositoryProvider).getIsAuthenticated();

    return Scaffold(
      appBar: AppBar(
        title: Text('Home Screen'),
      ),
      body: isAuth
          ?
          // Text("HI")
          AsyncValueWidget(
              value: ref.watch(fetchCollectionsProvider(ref)),
              data: (data) {
                return ListView.builder(
                  itemCount: data.length,
                  itemBuilder: (context, index) {
                    // return ListTile(
                    //   title: Text(data[index].id),
                    //   subtitle: Text(data[index].name),
                    // );
                    final item = data[index];
                    return Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(item.name),
                        Text(item.id),
                        ListView.builder(
                            shrinkWrap: true,
                            itemCount: item.todos.length,
                            itemBuilder: (context, index) {
                              final todo = item.todos[index];
                              return ListTile(
                                title: Text(todo.title),
                                subtitle: Text(todo.description),
                              );
                            })
                      ],
                    );
                  },
                );
              })
          : Text("Not Authenticated"),
    );
  }
}
