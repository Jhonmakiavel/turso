# Cómo usar el fork de Turso con rustls en tu app Tauri

## Opción 1: Usar directamente desde GitHub (Recomendado)

En el `Cargo.toml` de tu proyecto Tauri (normalmente en `src-tauri/Cargo.toml`), agrega o modifica la dependencia de turso:

```toml
[dependencies]
turso = { git = "https://github.com/Jhonmakiavel/turso.git", branch = "main", features = ["sync"] }
```

Si solo necesitas las funcionalidades básicas sin sync:

```toml
[dependencies]
turso = { git = "https://github.com/Jhonmakiavel/turso.git", branch = "main" }
```

## Opción 2: Usar un commit específico (Más estable)

Para asegurar que siempre uses la misma versión:

```toml
[dependencies]
turso = { git = "https://github.com/Jhonmakiavel/turso.git", rev = "4b837cd97", features = ["sync"] }
```

El `rev` es el hash del commit que acabamos de hacer.

## Opción 3: Usar una rama específica

Si creas una rama para desarrollo:

```toml
[dependencies]
turso = { git = "https://github.com/Jhonmakiavel/turso.git", branch = "android-rustls", features = ["sync"] }
```

## Configuración para Android en tu proyecto Tauri

### 1. Instalar los targets de Android

```bash
rustup target add aarch64-linux-android
rustup target add armv7-linux-androideabi
rustup target add i686-linux-android
rustup target add x86_64-linux-android
```

### 2. Configurar el NDK de Android

Asegúrate de tener el Android NDK instalado. Puedes instalarlo con Android Studio o descargarlo directamente.

Configura la variable de entorno:

```bash
# Windows (PowerShell)
$env:ANDROID_NDK_HOME = "C:\Users\TuUsuario\AppData\Local\Android\Sdk\ndk\27.0.12077973"

# Linux/Mac
export ANDROID_NDK_HOME="/path/to/android/ndk"
```

### 3. Compilar para Android

```bash
# Navega a tu proyecto Tauri
cd tu-proyecto-tauri

# Compila para Android
npm run tauri android build
# o
yarn tauri android build
# o
pnpm tauri android build
```

### 4. Desarrollo en Android

Para desarrollo y pruebas:

```bash
npm run tauri android dev
```

## Verificar que está usando rustls

Después de agregar la dependencia, ejecuta:

```bash
cd src-tauri
cargo tree -p turso | grep -E "rustls|openssl"
```

Deberías ver `rustls` y NO ver `openssl` en la salida.

## Actualizar a la última versión del fork

Cuando hagas más cambios en tu fork y quieras actualizar tu app:

```bash
cd src-tauri
cargo update -p turso
```

## Ejemplo completo de Cargo.toml

```toml
[package]
name = "mi-app-tauri"
version = "0.1.0"
edition = "2021"

[dependencies]
tauri = { version = "2.x", features = ["..."] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

# Tu fork de Turso con rustls
turso = { git = "https://github.com/Jhonmakiavel/turso.git", branch = "main", features = ["sync"] }

[features]
default = ["custom-protocol"]
custom-protocol = ["tauri/custom-protocol"]
```

## Solución de problemas

### Error: "failed to authenticate"

Si tienes problemas de autenticación con GitHub:

```bash
# Usar HTTPS en lugar de SSH
git config --global url."https://github.com/".insteadOf git@github.com:
```

### Error de compilación en Android

Si encuentras errores al compilar para Android, asegúrate de:

1. Tener el NDK instalado correctamente
2. Las variables de entorno configuradas
3. Los targets de Rust instalados

### Limpiar caché de Cargo

Si tienes problemas después de actualizar:

```bash
cd src-tauri
cargo clean
cargo update
cargo build
```

## Ventajas de usar rustls en Android

✅ No requiere compilar OpenSSL nativo  
✅ Mejor compatibilidad con PIE (Position Independent Executables)  
✅ Compilación más rápida  
✅ Binarios más pequeños  
✅ 100% Rust - mejor integración  
✅ Funciona en Android 15+ sin problemas  

## Próximos pasos

1. Agrega la dependencia a tu `Cargo.toml`
2. Ejecuta `cargo build` para verificar que compila
3. Prueba en Android con `tauri android dev`
4. Compila la APK final con `tauri android build`
