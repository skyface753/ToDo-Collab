// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'collection_repository.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

String _$collectionRepositoryHash() =>
    r'5bf758ce43272eabced9c8f37d91b7435b653c62';

/// See also [collectionRepository].
@ProviderFor(collectionRepository)
final collectionRepositoryProvider =
    AutoDisposeProvider<CollectionRepository>.internal(
  collectionRepository,
  name: r'collectionRepositoryProvider',
  debugGetCreateSourceHash: const bool.fromEnvironment('dart.vm.product')
      ? null
      : _$collectionRepositoryHash,
  dependencies: null,
  allTransitiveDependencies: null,
);

typedef CollectionRepositoryRef = AutoDisposeProviderRef<CollectionRepository>;
String _$fetchCollectionsHash() => r'492eee5421c15163a17daaf3f167518eb19caa6f';

/// Copied from Dart SDK
class _SystemHash {
  _SystemHash._();

  static int combine(int hash, int value) {
    // ignore: parameter_assignments
    hash = 0x1fffffff & (hash + value);
    // ignore: parameter_assignments
    hash = 0x1fffffff & (hash + ((0x0007ffff & hash) << 10));
    return hash ^ (hash >> 6);
  }

  static int finish(int hash) {
    // ignore: parameter_assignments
    hash = 0x1fffffff & (hash + ((0x03ffffff & hash) << 3));
    // ignore: parameter_assignments
    hash = hash ^ (hash >> 11);
    return 0x1fffffff & (hash + ((0x00003fff & hash) << 15));
  }
}

/// See also [fetchCollections].
@ProviderFor(fetchCollections)
const fetchCollectionsProvider = FetchCollectionsFamily();

/// See also [fetchCollections].
class FetchCollectionsFamily extends Family<AsyncValue<List<Collection>>> {
  /// See also [fetchCollections].
  const FetchCollectionsFamily();

  /// See also [fetchCollections].
  FetchCollectionsProvider call(
    WidgetRef ref2,
  ) {
    return FetchCollectionsProvider(
      ref2,
    );
  }

  @override
  FetchCollectionsProvider getProviderOverride(
    covariant FetchCollectionsProvider provider,
  ) {
    return call(
      provider.ref2,
    );
  }

  static const Iterable<ProviderOrFamily>? _dependencies = null;

  @override
  Iterable<ProviderOrFamily>? get dependencies => _dependencies;

  static const Iterable<ProviderOrFamily>? _allTransitiveDependencies = null;

  @override
  Iterable<ProviderOrFamily>? get allTransitiveDependencies =>
      _allTransitiveDependencies;

  @override
  String? get name => r'fetchCollectionsProvider';
}

/// See also [fetchCollections].
class FetchCollectionsProvider
    extends AutoDisposeFutureProvider<List<Collection>> {
  /// See also [fetchCollections].
  FetchCollectionsProvider(
    WidgetRef ref2,
  ) : this._internal(
          (ref) => fetchCollections(
            ref as FetchCollectionsRef,
            ref2,
          ),
          from: fetchCollectionsProvider,
          name: r'fetchCollectionsProvider',
          debugGetCreateSourceHash:
              const bool.fromEnvironment('dart.vm.product')
                  ? null
                  : _$fetchCollectionsHash,
          dependencies: FetchCollectionsFamily._dependencies,
          allTransitiveDependencies:
              FetchCollectionsFamily._allTransitiveDependencies,
          ref2: ref2,
        );

  FetchCollectionsProvider._internal(
    super._createNotifier, {
    required super.name,
    required super.dependencies,
    required super.allTransitiveDependencies,
    required super.debugGetCreateSourceHash,
    required super.from,
    required this.ref2,
  }) : super.internal();

  final WidgetRef ref2;

  @override
  Override overrideWith(
    FutureOr<List<Collection>> Function(FetchCollectionsRef provider) create,
  ) {
    return ProviderOverride(
      origin: this,
      override: FetchCollectionsProvider._internal(
        (ref) => create(ref as FetchCollectionsRef),
        from: from,
        name: null,
        dependencies: null,
        allTransitiveDependencies: null,
        debugGetCreateSourceHash: null,
        ref2: ref2,
      ),
    );
  }

  @override
  AutoDisposeFutureProviderElement<List<Collection>> createElement() {
    return _FetchCollectionsProviderElement(this);
  }

  @override
  bool operator ==(Object other) {
    return other is FetchCollectionsProvider && other.ref2 == ref2;
  }

  @override
  int get hashCode {
    var hash = _SystemHash.combine(0, runtimeType.hashCode);
    hash = _SystemHash.combine(hash, ref2.hashCode);

    return _SystemHash.finish(hash);
  }
}

mixin FetchCollectionsRef on AutoDisposeFutureProviderRef<List<Collection>> {
  /// The parameter `ref2` of this provider.
  WidgetRef get ref2;
}

class _FetchCollectionsProviderElement
    extends AutoDisposeFutureProviderElement<List<Collection>>
    with FetchCollectionsRef {
  _FetchCollectionsProviderElement(super.provider);

  @override
  WidgetRef get ref2 => (origin as FetchCollectionsProvider).ref2;
}
// ignore_for_file: type=lint
// ignore_for_file: subtype_of_sealed_class, invalid_use_of_internal_member, invalid_use_of_visible_for_testing_member
