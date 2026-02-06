# Migración de OpenSSL a rustls para Android

## Cambios realizados

### 1. Actualización de dependencias en `bindings/rust/Cargo.toml`

- **Reemplazado**: `hyper-tls = { version = "0.6.0", optional = true }`
- **Por**: `hyper-rustls = { version = "0.27", features = ["http1", "native-tokio", "ring"], optional = true }`

- **Actualizado**: `reqwest = { version = "0.12.28", features = ["json"] }`
- **A**: `reqwest = { version = "0.12.28", default-features = false, features = ["json", "rustls-tls"] }`

- **Actualizado feature sync**: Cambió `dep:hyper-tls` por `dep:hyper-rustls`

### 2. Actualización del código en `bindings/rust/src/sync.rs`

- **Imports actualizados**:
  - Reemplazado: `use hyper_tls::HttpsConnector;`
  - Por: `use hyper_rustls::HttpsConnectorBuilder;`

- **Creación del cliente HTTPS**:
  ```rust
  // Antes:
  let mut http_connector = HttpConnector::new();
  http_connector.enforce_http(false);
  let https: HttpsConnector<HttpConnector> = HttpsConnector::new();
  let client: Client<HttpsConnector<HttpConnector>, Full<Bytes>> =
      Client::builder(TokioExecutor::new()).build::<_, Full<Bytes>>(https);

  // Después:
  let https = HttpsConnectorBuilder::new()
      .with_native_roots()
      .expect("failed to load native root certificates")
      .https_or_http()
      .enable_http1()
      .build();
  
  let client = Client::builder(TokioExecutor::new()).build::<_, Full<Bytes>>(https);
  ```

- **Firma de función genérica**: La función `process_http` ahora usa un tipo genérico para el conector, haciéndola más flexible.

## Beneficios de rustls para Android

1. **Sin dependencias nativas**: No requiere compilar OpenSSL para Android
2. **Mejor compatibilidad PIE**: Funciona correctamente con Position Independent Executables
3. **Compilación más rápida**: No necesita compilar código C
4. **Binarios más pequeños**: rustls es más ligero que OpenSSL
5. **100% Rust**: Mejor integración con el ecosistema Rust

## Compilación para Android

### Instalar targets de Android:
```bash
rustup target add aarch64-linux-android
rustup target add armv7-linux-androideabi
rustup target add i686-linux-android
rustup target add x86_64-linux-android
```

### Compilar para Android (ejemplo con aarch64):
```bash
cargo build --target aarch64-linux-android --release
```

### Compilar con la feature sync:
```bash
cargo build --target aarch64-linux-android --release --features sync
```

## Notas importantes

- La configuración de Android en `.cargo/config.toml` ya incluye los flags necesarios para Android 15+ (16KB page alignment)
- rustls usa certificados nativos del sistema con `with_native_roots()`
- El conector soporta tanto HTTP como HTTPS con `.https_or_http()`

## Verificación

Para verificar que los cambios funcionan correctamente:

```bash
# Verificar que compila sin errores
cargo check --target aarch64-linux-android --features sync

# Ejecutar tests (si están disponibles)
cargo test --features sync
```

## Próximos pasos

1. Probar la compilación para todos los targets de Android
2. Verificar que las conexiones HTTPS funcionan correctamente
3. Realizar pruebas de integración con el servidor de sincronización
4. Actualizar la documentación del proyecto si es necesario
