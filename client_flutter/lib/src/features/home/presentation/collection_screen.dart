import 'dart:convert';

import 'package:client_flutter/src/common_widgets/async_value_widget.dart';
import 'package:client_flutter/src/features/home/domain/collection.dart';
import 'package:client_flutter/src/features/home/presentation/collection_controller.dart';
import 'package:client_flutter/src/utils/logger.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class CollectionScreen extends ConsumerStatefulWidget {
  const CollectionScreen({required this.collectionId, super.key});
  final String collectionId;

  @override
  CollectionScreenState createState() => CollectionScreenState();
}

class CollectionScreenState extends ConsumerState<CollectionScreen> {
  final TextEditingController _titleController = TextEditingController();
  final TextEditingController _descriptionController = TextEditingController();
  WebSocketChannel? _channel;
  late CollectionController _collectionController;
  final ScrollController _scrollController = ScrollController();

  void _listen() {
    if (_channel != null) {
      _channel!.stream.listen((event) {
        try {
          final json = jsonDecode(event as String);
          final todo = Todo.fromJson(json as Map<String, dynamic>);
          _collectionController.addTodoToCollectionTodos(todo);
        } catch (e) {
          logger.e('collection_screen._listen: $e');
        }
      });
    }
  }

  @override
  void initState() {
    super.initState();
    _collectionController = ref.read(collectionControllerProvider.notifier);
    _collectionController.getCollection(widget.collectionId);
  }

  @override
  Widget build(BuildContext context) {
    // final state = ref.watch(collectionControllerProvider);
    // if(state.value == null) {
    //   return const Center(child: CircularProgressIndicator());
    // }
    final state = ref.watch(collectionControllerProvider);
    return Scaffold(
      appBar: AppBar(
        title: Text(state.value?.name ?? 'Loading...'),
      ),
      body: AsyncValueWidget(
        value: state,
        data: (collection) {
          if (collection == null) {
            return const Center(child: CircularProgressIndicator());
          }
          // if (collection.todos == null) {
          //   return const Text('No todos');
          // }
          // if (collection.todos!.isEmpty) {
          //   return const Text('Todos is empty');
          // }
          if (collection.websocketUrl != null) {
            if (_channel != null) {
              _channel!.sink.close();
            }
            _channel = WebSocketChannel.connect(
              Uri.parse(collection.websocketUrl!),
            );
            _listen();
          } else {
            return const Text('No websocketUrl');
          }
          return Column(
            children: [
              Expanded(
                child: Align(
                  alignment: Alignment.topCenter,
                  child: ListView.builder(
                    controller: _scrollController,
                    reverse: true,
                    shrinkWrap: true,
                    itemCount: collection.todos!.length,
                    itemBuilder: (context, index) {
                      return ListTile(
                        title: Text(collection.todos![index].title),
                        subtitle: Text(collection.todos![index].description),
                      );
                    },
                  ),
                ),
              ),
              TextField(
                controller: _titleController,
                decoration: const InputDecoration(
                  labelText: 'Title',
                ),
              ),
              TextField(
                controller: _descriptionController,
                decoration: const InputDecoration(
                  labelText: 'Description',
                ),
              ),
              ElevatedButton(
                onPressed: () {
                  _channel!.sink.add(
                    jsonEncode(
                      {
                        'title': _titleController.text,
                        'description': _descriptionController.text,
                      },
                    ),
                  );
                  _titleController.clear();
                  _descriptionController.clear();
                },
                child: const Text('Add'),
              ),
            ],
          );
        },
      ),
    );
  }
}
