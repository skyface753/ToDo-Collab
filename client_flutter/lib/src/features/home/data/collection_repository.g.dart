// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'collection_repository.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

String _$collectionRepositoryHash() =>
    r'9e04e484d5dfe7a6b5af7912451af1040c693d02';

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
String _$fetchCollectionsHash() => r'f77c1c395ac23372c2db59a2fc39220932050dee';

/// See also [fetchCollections].
@ProviderFor(fetchCollections)
final fetchCollectionsProvider =
    AutoDisposeFutureProvider<List<Collection>>.internal(
  fetchCollections,
  name: r'fetchCollectionsProvider',
  debugGetCreateSourceHash: const bool.fromEnvironment('dart.vm.product')
      ? null
      : _$fetchCollectionsHash,
  dependencies: null,
  allTransitiveDependencies: null,
);

typedef FetchCollectionsRef = AutoDisposeFutureProviderRef<List<Collection>>;
String _$fetchCollectionHash() => r'a201529694b6c7cdafc852ac13b1b24dcaec7948';

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

/// See also [fetchCollection].
@ProviderFor(fetchCollection)
const fetchCollectionProvider = FetchCollectionFamily();

/// See also [fetchCollection].
class FetchCollectionFamily extends Family<AsyncValue<Collection>> {
  /// See also [fetchCollection].
  const FetchCollectionFamily();

  /// See also [fetchCollection].
  FetchCollectionProvider call(
    String collectionId,
  ) {
    return FetchCollectionProvider(
      collectionId,
    );
  }

  @override
  FetchCollectionProvider getProviderOverride(
    covariant FetchCollectionProvider provider,
  ) {
    return call(
      provider.collectionId,
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
  String? get name => r'fetchCollectionProvider';
}

/// See also [fetchCollection].
class FetchCollectionProvider extends AutoDisposeFutureProvider<Collection> {
  /// See also [fetchCollection].
  FetchCollectionProvider(
    String collectionId,
  ) : this._internal(
          (ref) => fetchCollection(
            ref as FetchCollectionRef,
            collectionId,
          ),
          from: fetchCollectionProvider,
          name: r'fetchCollectionProvider',
          debugGetCreateSourceHash:
              const bool.fromEnvironment('dart.vm.product')
                  ? null
                  : _$fetchCollectionHash,
          dependencies: FetchCollectionFamily._dependencies,
          allTransitiveDependencies:
              FetchCollectionFamily._allTransitiveDependencies,
          collectionId: collectionId,
        );

  FetchCollectionProvider._internal(
    super._createNotifier, {
    required super.name,
    required super.dependencies,
    required super.allTransitiveDependencies,
    required super.debugGetCreateSourceHash,
    required super.from,
    required this.collectionId,
  }) : super.internal();

  final String collectionId;

  @override
  Override overrideWith(
    FutureOr<Collection> Function(FetchCollectionRef provider) create,
  ) {
    return ProviderOverride(
      origin: this,
      override: FetchCollectionProvider._internal(
        (ref) => create(ref as FetchCollectionRef),
        from: from,
        name: null,
        dependencies: null,
        allTransitiveDependencies: null,
        debugGetCreateSourceHash: null,
        collectionId: collectionId,
      ),
    );
  }

  @override
  AutoDisposeFutureProviderElement<Collection> createElement() {
    return _FetchCollectionProviderElement(this);
  }

  @override
  bool operator ==(Object other) {
    return other is FetchCollectionProvider &&
        other.collectionId == collectionId;
  }

  @override
  int get hashCode {
    var hash = _SystemHash.combine(0, runtimeType.hashCode);
    hash = _SystemHash.combine(hash, collectionId.hashCode);

    return _SystemHash.finish(hash);
  }
}

mixin FetchCollectionRef on AutoDisposeFutureProviderRef<Collection> {
  /// The parameter `collectionId` of this provider.
  String get collectionId;
}

class _FetchCollectionProviderElement
    extends AutoDisposeFutureProviderElement<Collection>
    with FetchCollectionRef {
  _FetchCollectionProviderElement(super.provider);

  @override
  String get collectionId => (origin as FetchCollectionProvider).collectionId;
}
// ignore_for_file: type=lint
// ignore_for_file: subtype_of_sealed_class, invalid_use_of_internal_member, invalid_use_of_visible_for_testing_member
