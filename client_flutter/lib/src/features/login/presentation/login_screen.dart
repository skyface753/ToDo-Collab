import 'package:client_flutter/src/features/home/data/collection_repository.dart';
import 'package:client_flutter/src/features/login/presentation/user_controller.dart';
import 'package:client_flutter/src/routing/app_router.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';

class LoginScreen extends StatefulHookConsumerWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<ConsumerStatefulWidget> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  TextEditingController username = TextEditingController();
  TextEditingController password = TextEditingController();
  bool _isHidden = true;

  @override
  void initState() {
    username.text = 'test'; //innitail value of text field
    password.text = 'Test123';
    super.initState();
  }

  void _togglePasswordView() {
    setState(() {
      _isHidden = !_isHidden;
    });
  }

  void showSnackbar(BuildContext context, String text) {
    final snackBar = SnackBar(
      content: Text(text),
      duration: const Duration(seconds: 5),
    );
    ScaffoldMessenger.of(context).showSnackBar(snackBar);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login Page'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(30),
        child: Column(
          children: [
            TextField(
              controller: username,
              decoration: const InputDecoration(
                labelText: 'Username',
                icon: Icon(Icons.people), //icon at head of input
              ),
            ),
            TextField(
              controller: password,
              obscureText: _isHidden,
              decoration: InputDecoration(
                icon: const Icon(Icons.lock), //icon at head of input
                //prefixIcon: Icon(Icons.people), //you can use prefixIcon property too.
                labelText: 'Password',
                suffixIcon: IconButton(
                  onPressed: _togglePasswordView,
                  icon: Icon(
                    _isHidden ? Icons.visibility : Icons.visibility_off,
                  ),
                ), //icon at tail of input
              ),
            ),
            const SizedBox(height: 20),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: () {
                      ref
                          .read(userControllerProvider.notifier)
                          .login(
                            username: username.text,
                            password: password.text,
                          )
                          .then(
                            (res) => {
                              res.fold(
                                (l) => {
                                  showSnackbar(context, l),
                                },
                                (r) => {
                                  ref.invalidate(fetchCollectionsProvider),
                                  context
                                      .goNamed(TopLevelDestinations.home.name),
                                },
                              ),
                            },
                          );
                    },
                    child: const Text('Login'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
