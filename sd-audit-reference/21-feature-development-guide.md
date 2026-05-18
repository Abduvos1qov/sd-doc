# 21 — Feature development guide

Step-by-step recipe to add a new feature. We'll use a hypothetical
**VisitNotes** feature throughout: a screen that lists "visit notes"
(per-client, free-text reminders) and lets the user add/delete them
locally with eventual server sync.

> The codebase already has a `NoteBox` for in-visit notes — this
> example uses a *different* entity (`VisitNoteBox`) to keep the walk
> through honest about creating every layer from scratch. In practice
> you'd reuse `NoteBox` here.

The 13 steps map to where files live. Skim before starting; don't
skip the registration step at the end.

## 1. Add a domain entity

**File:** `lib/features/sd_audit/domain/entities/visit_note_entity.dart`

```dart
class VisitNoteEntity {
  final String id;
  final String clientId;
  final String text;
  final DateTime createdAt;

  const VisitNoteEntity({
    required this.id,
    required this.clientId,
    required this.text,
    required this.createdAt,
  });
}
```

Plain Dart. No annotations, no JSON parsing here. (JSON parsing
lives on the response model in `data/model/` or
`domain/models/response_models/`.)

## 2. Add a repository interface

**File:** `lib/features/sd_audit/domain/repositories/visit_note_repository.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:sdaudit/features/sd_audit/core/error/failure.dart';
import 'package:sdaudit/features/sd_audit/domain/entities/visit_note_entity.dart';

abstract class VisitNoteRepository {
  Future<Either<Failure, List<VisitNoteEntity>>> getNotes(String clientId);
  Future<Either<Failure, VisitNoteEntity>> addNote({
    required String clientId,
    required String text,
  });
  Future<Either<Failure, bool>> deleteNote(String id);
}
```

Every method returns `Either<Failure, T>`.

## 3. Add use cases

One per repo method. All in `lib/features/sd_audit/domain/usecases/`.

```dart
// get_visit_notes_usecase.dart
class GetVisitNotesUsecase {
  final VisitNoteRepository _repo;
  GetVisitNotesUsecase(this._repo);
  Future<Either<Failure, List<VisitNoteEntity>>> call(String clientId)
      => _repo.getNotes(clientId);
}

// add_visit_note_usecase.dart
class AddVisitNoteParam {
  final String clientId;
  final String text;
  const AddVisitNoteParam({required this.clientId, required this.text});
}

class AddVisitNoteUsecase {
  final VisitNoteRepository _repo;
  AddVisitNoteUsecase(this._repo);
  Future<Either<Failure, VisitNoteEntity>> call(AddVisitNoteParam p)
      => _repo.addNote(clientId: p.clientId, text: p.text);
}

// delete_visit_note_usecase.dart
class DeleteVisitNoteUsecase {
  final VisitNoteRepository _repo;
  DeleteVisitNoteUsecase(this._repo);
  Future<Either<Failure, bool>> call(String id) => _repo.deleteNote(id);
}
```

A use case is almost always a 1:1 forward. The indirection is so
BLoCs can mock per-action, not per-repo.

## 4. Add a data-source method (remote)

If the feature needs server I/O, append to
`lib/features/sd_audit/data/data_sources/remote_data_source/remote_data_sources.dart`.

In the abstract:

```dart
Future<Response> getVisitNotes(String clientId);
Future<Response> postVisitNote({required String clientId, required String text});
Future<Response> deleteVisitNote(String id);
```

In the `Impl`:

```dart
@override
Future<Response> getVisitNotes(String clientId) {
  return httpClient.getRequestWithParams(
    serverUrl,
    '/api3/auditor/visitNotes',
    {'client_id': clientId, 'token': token},
  );
}
```

Append `'/api3/auditor/visitNotes'` (or wherever the API lives) to
`lib/common/constants/end_points.dart` if you prefer constant-based
references.

## 5. Add a repository impl

**File:** `lib/features/sd_audit/data/repositories/visit_note_repository_impl.dart`

```dart
class VisitNoteRepositoryImpl extends BaseRepositoryImpl
    implements VisitNoteRepository {
  final RemoteDataSources remoteData;

  VisitNoteRepositoryImpl({
    required this.remoteData,
    required NetworkInfo networkInfo,
  }) : super(networkInfo);

  @override
  Future<Either<Failure, List<VisitNoteEntity>>> getNotes(String clientId)
      => workWithServer(() async {
        // For a purely local feature: workWithLocal(() async { ... })
        final response = await remoteData.getVisitNotes(clientId);
        final list = (response.data['notes'] as List)
            .map((j) => VisitNoteEntity(
                  id: j['id'],
                  clientId: j['client_id'],
                  text: j['text'],
                  createdAt: DateTime.parse(j['created_at']),
                ))
            .toList();
        return list;
      });

  @override
  Future<Either<Failure, VisitNoteEntity>> addNote({
    required String clientId,
    required String text,
  }) => workWithServer(() async {
        final response = await remoteData.postVisitNote(
          clientId: clientId, text: text);
        final j = response.data;
        return VisitNoteEntity(
          id: j['id'],
          clientId: j['client_id'],
          text: j['text'],
          createdAt: DateTime.parse(j['created_at']),
        );
      });

  @override
  Future<Either<Failure, bool>> deleteNote(String id)
      => workWithServer(() async {
        await remoteData.deleteVisitNote(id);
        return true;
      });
}
```

Extends `BaseRepositoryImpl`. Uses `workWithServer` for any call
that talks to the network. Never `try/catch` here.

## 6. Add an ObjectBox model (if local persistence is needed)

**File:** `lib/db/models/visit_note_model.dart`

```dart
import 'package:objectbox/objectbox.dart';

@Entity()
class VisitNoteBox {
  @Id()
  int boxId;
  String id;        // server id
  String clientId;
  String text;
  @Property(type: PropertyType.date)
  DateTime createdAt;

  VisitNoteBox({
    this.boxId = 0,
    required this.id,
    required this.clientId,
    required this.text,
    required this.createdAt,
  });
}
```

Then:

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

Apply the manual `objectbox.g.dart` fix per
[`18-build-and-deploy.md`](18-build-and-deploy.md) if codegen produces
nullable `ToMany`.

Add a `Box<VisitNoteBox>` field to the `ObjectBox` class
(`lib/db/objectbox/object_box.dart`) and accessor methods:

```dart
late final Box<VisitNoteBox> _visitNoteBox;
// in _create constructor:
_visitNoteBox = Box<VisitNoteBox>(store);

List<VisitNoteBox> getVisitNotes(String clientId) =>
  _visitNoteBox.query(VisitNoteBox_.clientId.equals(clientId)).build().find();

int putVisitNote(VisitNoteBox note) => _visitNoteBox.put(note);
bool removeVisitNote(int boxId) => _visitNoteBox.remove(boxId);
```

## 7. Add a mapper

**File:** `lib/features/sd_audit/data/mapper/visit_note_mapper.dart`

```dart
class VisitNoteMapper {
  static VisitNoteBox entityToBox(VisitNoteEntity e) => VisitNoteBox(
    id: e.id, clientId: e.clientId, text: e.text, createdAt: e.createdAt,
  );

  static VisitNoteEntity boxToEntity(VisitNoteBox b) => VisitNoteEntity(
    id: b.id, clientId: b.clientId, text: b.text, createdAt: b.createdAt,
  );
}
```

Static methods, `{source}To{target}` naming.

## 8. Create the BLoC trio

**Folder:** `lib/features/sd_audit/presentation/bloc/visit_note/`

```dart
// visit_note_event.dart
part of 'visit_note_bloc.dart';
abstract class VisitNoteEvent { const VisitNoteEvent(); }
class VisitNoteLoadEvent extends VisitNoteEvent {
  final String clientId;
  const VisitNoteLoadEvent({required this.clientId});
}
class VisitNoteAddEvent extends VisitNoteEvent {
  final String clientId; final String text;
  const VisitNoteAddEvent({required this.clientId, required this.text});
}
class VisitNoteDeleteEvent extends VisitNoteEvent {
  final String id;
  const VisitNoteDeleteEvent({required this.id});
}
```

```dart
// visit_note_state.dart
part of 'visit_note_bloc.dart';
abstract class VisitNoteState { const VisitNoteState(); }
class VisitNoteInitial   extends VisitNoteState {}
class VisitNoteLoading   extends VisitNoteState {}
class VisitNoteLoaded    extends VisitNoteState {
  final List<VisitNoteEntity> notes;
  const VisitNoteLoaded({required this.notes});
}
class VisitNoteError extends VisitNoteState {
  final String error;
  const VisitNoteError({required this.error});
}
```

```dart
// visit_note_bloc.dart
import 'package:bloc/bloc.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:sdaudit/features/sd_audit/domain/entities/visit_note_entity.dart';
import 'package:sdaudit/features/sd_audit/domain/usecases/get_visit_notes_usecase.dart';
import 'package:sdaudit/features/sd_audit/domain/usecases/add_visit_note_usecase.dart';
import 'package:sdaudit/features/sd_audit/domain/usecases/delete_visit_note_usecase.dart';

part 'visit_note_event.dart';
part 'visit_note_state.dart';

class VisitNoteBloc extends Bloc<VisitNoteEvent, VisitNoteState> {
  final GetVisitNotesUsecase _get;
  final AddVisitNoteUsecase _add;
  final DeleteVisitNoteUsecase _delete;
  List<VisitNoteEntity> _current = [];

  VisitNoteBloc({
    required GetVisitNotesUsecase getUsecase,
    required AddVisitNoteUsecase addUsecase,
    required DeleteVisitNoteUsecase deleteUsecase,
  })  : _get = getUsecase,
        _add = addUsecase,
        _delete = deleteUsecase,
        super(VisitNoteInitial()) {

    on<VisitNoteLoadEvent>((event, emit) async {
      emit(VisitNoteLoading());
      final result = await _get.call(event.clientId);
      result.fold(
        (l) => emit(VisitNoteError(error: l.message.tr())),
        (r) { _current = r; emit(VisitNoteLoaded(notes: r)); },
      );
    });

    on<VisitNoteAddEvent>((event, emit) async {
      final result = await _add.call(
        AddVisitNoteParam(clientId: event.clientId, text: event.text));
      result.fold(
        (l) => emit(VisitNoteError(error: l.message.tr())),
        (r) { _current = [..._current, r];
              emit(VisitNoteLoaded(notes: _current)); },
      );
    });

    on<VisitNoteDeleteEvent>((event, emit) async {
      final result = await _delete.call(event.id);
      result.fold(
        (l) => emit(VisitNoteError(error: l.message.tr())),
        (_) { _current = _current.where((n) => n.id != event.id).toList();
              emit(VisitNoteLoaded(notes: _current)); },
      );
    });
  }
}
```

## 9. Create the page

**File:** `lib/features/sd_audit/presentation/pages/visit_note_screen.dart`

```dart
class VisitNoteScreen extends StatefulWidget {
  final String clientId;
  const VisitNoteScreen({super.key, required this.clientId});

  @override
  State<VisitNoteScreen> createState() => _VisitNoteScreenState();
}

class _VisitNoteScreenState extends State<VisitNoteScreen> {
  late final VisitNoteBloc _bloc;
  final _controller = TextEditingController();

  @override
  void initState() {
    super.initState();
    _bloc = context.read<VisitNoteBloc>();
    _bloc.add(VisitNoteLoadEvent(clientId: widget.clientId));
  }

  @override
  void dispose() { _controller.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: _buildAppBar(),
        body: _buildBody(),
        floatingActionButton: _buildAddFab(),
      );

  PreferredSizeWidget _buildAppBar() =>
      AppBar(title: Text('visit_notes_title'.tr()));

  Widget _buildBody() => BlocConsumer<VisitNoteBloc, VisitNoteState>(
        listener: (context, state) {
          if (state is VisitNoteError) {
            // snackbar...
          }
        },
        buildWhen: (_, curr) =>
          curr is VisitNoteLoaded || curr is VisitNoteLoading,
        builder: (context, state) {
          if (state is VisitNoteLoading) {
            return const Center(child: CircularProgressIndicator());
          }
          if (state is VisitNoteLoaded) {
            return ListView.builder(
              itemCount: state.notes.length,
              itemBuilder: (_, i) => _buildRow(state.notes[i]),
            );
          }
          return const SizedBox.shrink();
        },
      );

  Widget _buildRow(VisitNoteEntity n) => ListTile(
        title: Text(n.text),
        trailing: IconButton(
          icon: const Icon(Icons.delete_outline),
          onPressed: () => _bloc.add(VisitNoteDeleteEvent(id: n.id)),
        ),
      );

  Widget _buildAddFab() => FloatingActionButton(
        onPressed: () { /* open dialog with _controller, then add event */ },
        child: const Icon(Icons.add),
      );
}
```

`StatefulWidget`, `late final _bloc`, private `_build*` methods.

## 10. Register everything in `lib/injection_container.dart`

Order: data sources → repository → use cases → BLoC.

```dart
// data source — already registered (RemoteDataSources)
// repository
getIt.registerFactory<VisitNoteRepository>(
  () => VisitNoteRepositoryImpl(remoteData: getIt(), networkInfo: getIt()),
);
// use cases
getIt.registerLazySingleton(() => GetVisitNotesUsecase(getIt()));
getIt.registerLazySingleton(() => AddVisitNoteUsecase(getIt()));
getIt.registerLazySingleton(() => DeleteVisitNoteUsecase(getIt()));
// bloc
getIt.registerFactory(() => VisitNoteBloc(
      getUsecase: getIt(),
      addUsecase: getIt(),
      deleteUsecase: getIt(),
    ));
```

If you flip this order — register the bloc before its use cases —
the first resolution throws at runtime.

## 11. Wire the BLoC into `main.dart`

If the BLoC needs global availability (any page can read it), add it
to the `MultiBlocProvider`:

```dart
BlocProvider<VisitNoteBloc>(create: (_) => getIt()),
```

If only one screen uses it (more common), skip `main.dart` and wrap
the screen at the call site:

```dart
Navigator.push(context, MaterialPageRoute(builder: (_) =>
  BlocProvider<VisitNoteBloc>(
    create: (_) => getIt(),
    child: VisitNoteScreen(clientId: id),
  ),
));
```

Local provision is preferred — fewer global instances.

## 12. Add translations

Append the keys you used (`visit_notes_title`, etc.) to:

- `assets/translations/uz.json`
- `assets/translations/ru.json`
- `assets/translations/en.json`

`.tr()` reads at runtime; no codegen.

## 13. Write tests

`test/features/sd_audit/presentation/bloc/visit_note/visit_note_bloc_test.dart`
with `mocktail` + `bloc_test`. Pattern is in
[`19-testing.md`](19-testing.md).

```dart
class MockGet extends Mock implements GetVisitNotesUsecase {}
class MockAdd extends Mock implements AddVisitNoteUsecase {}
class MockDel extends Mock implements DeleteVisitNoteUsecase {}

void main() {
  late VisitNoteBloc bloc;
  late MockGet get; late MockAdd add; late MockDel del;
  setUp(() {
    get = MockGet(); add = MockAdd(); del = MockDel();
    bloc = VisitNoteBloc(
      getUsecase: get, addUsecase: add, deleteUsecase: del);
  });
  tearDown(() => bloc.close());

  blocTest<VisitNoteBloc, VisitNoteState>(
    'load → [Loading, Loaded]',
    build: () {
      when(() => get.call(any()))
          .thenAnswer((_) async => const Right(<VisitNoteEntity>[]));
      return bloc;
    },
    act: (b) => b.add(const VisitNoteLoadEvent(clientId: 'c1')),
    expect: () => [isA<VisitNoteLoading>(), isA<VisitNoteLoaded>()],
  );
}
```

## Done — quick checklist

```
☐ Entity              in domain/entities/
☐ Repository iface    in domain/repositories/
☐ Use cases (3)       in domain/usecases/
☐ Endpoint constants  in lib/common/constants/end_points.dart
☐ Remote DS methods   in data/data_sources/remote_data_source/
☐ Repository impl     in data/repositories/  extends BaseRepositoryImpl
☐ ObjectBox model     in lib/db/models/  +  codegen  +  manual edit
☐ ObjectBox accessors in lib/db/objectbox/object_box.dart
☐ Mapper              in data/mapper/
☐ BLoC trio           in presentation/bloc/{feature}/
☐ Page                in presentation/pages/
☐ DI registrations    in lib/injection_container.dart (correct order)
☐ BlocProvider wiring in main.dart MultiBlocProvider or locally
☐ Translations        in assets/translations/{en,uz,ru}.json
☐ Tests               in test/features/sd_audit/...
```

Reuse where possible — most "new features" extend an existing one
rather than starting from scratch. Don't add a new repo for one
method that fits an existing one.
