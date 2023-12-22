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
// ignore_for_file: type=lint
// ignore_for_file: subtype_of_sealed_class, invalid_use_of_internal_member, invalid_use_of_visible_for_testing_member
