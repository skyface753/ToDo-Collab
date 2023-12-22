import 'package:client_flutter/src/common_widgets/async_value_widget.dart';
import 'package:client_flutter/src/features/home/data/collection_repository.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class CollectionScreen extends ConsumerStatefulWidget {
  const CollectionScreen({required this.collectionId, super.key});
  final String collectionId;

  @override
  CollectionScreenState createState() => CollectionScreenState();
}

class CollectionScreenState extends ConsumerState<CollectionScreen> {
  @override
  Widget build(BuildContext context) {
    final collection = ref.watch(fetchCollectionProvider(widget.collectionId));
    return Scaffold(
      appBar: AppBar(
        title: Text(collection.value?.name ?? 'Loading...'),
      ),
      body: AsyncValueWidget(
        value: collection,
        data: (data) {
          if (data.todos == null) {
            return const Text('No todos');
          }
          if (data.todos!.isEmpty) {
            return const Text('Todos is empty');
          }
          return ListView.builder(
            itemCount: data.todos!.length,
            itemBuilder: (context, index) {
              return ListTile(
                title: Text(data.todos![index].title),
                subtitle: Text(data.todos![index].description),
              );
            },
          );
        },
      ),
    );
  }
}
