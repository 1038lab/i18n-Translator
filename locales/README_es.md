# GitHub i18n Acciones Traducción automática

## 🌍 Idiomas disponibles

| 🌐 Idioma | 📄 Archivo | 📊 Estado |
|:-----------|:--------|:----------|
| Inglés | [README_en.md](./README_en.md) | ✅ Disponible |
| Inglés | [README_en.md](./README_en.md) | ✅ Disponible |
| Chino (中文) | [README_zh.md](./README_zh.md) | ✅ Disponible |
| Japonés (日本語) | [README_ja.md](./README_ja.md) | ✅ Disponible |
| Coreano (한국어) | [README_ko.md](./README_ko.md) | ✅ Disponible |
| Español (Español) | [README_es.md](./README_es.md) | ✅ Disponible |
| Francés (Français) | [README_fr.md](./README_fr.md) | ✅ Disponible |
| Ruso (Русский) | [README_ru.md](./README_ru.md) | ✅ Disponible |

## 📋 **Descripción general**

Esta guía le ayudará a configurar rápidamente un sistema de traducción automática de acciones GitHub utilizando nuestras herramientas proporcionadas para traducir automáticamente archivos README.md de inglés a varios idiomas.

**🆓 Ahora ofrecemos DOS modos de traducción:**
- **Modo libre** (recomendado): Sin configuración, no se necesita la clave API
- **Modo API**: Mayor precisión con Google Translate API (requiere la clave API)

### **Características**
- ✅ **Dos modos de traducción**: Gratuito (sin configuración) y API (alta calidad)
- ✅ Detecta automáticamente las actualizaciones de README.md y activa la traducción
- ✅ Admite varios idiomas de destino (chino, japonés, coreano, español, etc.)
- ✅ Evita que los términos técnicos se traduzcan
- ✅ Mantiene el formato completo de Markdown
- ✅ Gestión segura de claves API (solo en modo API)
- ✅ Traducción incremental (solo traduce contenido actualizado)
- ✅ Navegación intuitiva por idiomas
- ✅ Botón de encendido/apagado para ahorrar costes de API
- ✅ Protección inteligente contra sobrescritura (4 modos)
- ✅ Detección y protección manual de ediciones
- ✅ Activación manual del flujo de trabajo con opciones de forzado

---

## 🆓 **Inicio rápido (modo gratuito - recomendado)**

### **Paso 1: Copiar archivos del proyecto**
Copie los siguientes archivos del proyecto [i18n](https://github.com/1038lab/i18n) a su proyecto:

__CÓDIGO_0__

### **Paso 2: Ejecutar traducción libre**
1. En el repositorio GitHub, haz clic en la pestaña **"Acciones"**
2. Selecciona el flujo de trabajo **"Traducción automática de README (gratuita)"**
3. Haz clic en **"Ejecutar flujo de trabajo"** → Selecciona la rama `main` → Haz clic en **"Ejecutar flujo de trabajo"**
4. Espera a que finalice y revisa la carpeta `locales/` para ver los archivos traducidos.

**¡Listo! No necesitas la clave API.**

---

## 💰 **Actualizar al modo API (opcional - mayor calidad)**

Si desea una mayor precisión de traducción, puede actualizar al modo API:

## 🚀 **Paso 1: Configurar Google Cloud Translation API**

### **1.1 Crear un proyecto de Google Cloud**
1. Visita [Google Cloud Console](https://console.cloud.google.com/)
2. Haz clic en el selector de proyectos y crea uno nuevo.
3. Introduce el nombre del proyecto (p. ej., `readme-translator`).
4. Haz clic en "Crear".

### **1.2 Habilitar la traducción API**
1. En Google Cloud Console, asegúrate de haber seleccionado el proyecto correcto.
2. Busca "Cloud Translation API" en la barra de búsqueda.
3. Haz clic en el resultado "Cloud Translation API".
4. Haz clic en el botón "Habilitar".
5. Espera a que se habilite API.

### **1.3 Crear clave API**
1. Vaya a "APIs & Services" → "Credentials"
2. Haga clic en "Create Credentials" → "API Key"
3. Copie la clave API generada (formato similar a: `AIzaSyC...`)
4. **Importante**: Guarde esta clave inmediatamente, la necesitará más adelante.

### **1.4 Restringir los permisos de la clave API (Recomendado)**
1. En la página Credenciales, haga clic en la clave API que acaba de crear.
2. En la sección "Restricciones de API":
- Seleccione "Restringir clave".
- Marque "Traducción en la nube API".
3. Haga clic en "Guardar".

---

## 🔐 **Paso 2: Configurar API Ingrese GitHub**

### **2.1 Establecer la clave secreta del repositorio**
1. En el repositorio GitHub, haz clic en la pestaña **"Configuración"**
2. En el menú de la izquierda, selecciona **"Secretos y variables"** → **"Acciones"**
3. Haz clic en **"Nueva clave secreta del repositorio"**
4. Completa la información:
- **Nombre**: `GOOGLE_TRANSLATE_API_KEY`
- **Secreto**: Pega la clave API que obtuviste en el paso 1.3
5. Haz clic en **"Añadir clave secreta"**

### **2.2 Verificar la configuración del secreto**
Después de la configuración, debería ver en la lista de secretos:
```
GOOGLE_TRANSLATE_API_KEY    Updated now
```

---

## 📁 **Paso 3: Cambiar al modo API**

### **3.1 Actualizar configuración**
Abre `.github/i18n-config.yml` y cambia el modo:

__CÓDIGO_2__

### **3.2 Descripciones de archivos**
- **`i18n-config.yml`** - Archivo de configuración de traducción, controla idiomas, protección de términos, etc.
- **`translate-readme-api.yml`** - Archivo de flujo de trabajo de acciones en modo API GitHub
- **`translate-readme-free.yml`** - Archivo de flujo de trabajo de acciones en modo libre GitHub
- **`translate_readme_api.py`** - Script de traducción API
- **`translate_readme_free.py`** - Script de traducción libre

---

## ⚙️ **Paso 4: Configurar los ajustes de traducción**

### **4.1 Editar archivo de configuración**
Abra el archivo `.github/i18n-config.yml` y modifíquelo según sea necesario:

#### **Seleccionar modo de traducción**
```yaml
translation:
  enabled: true           # Set to false to disable translation
  mode: "free"           # "free" (no API key) or "api" (higher quality)
```

#### **Seleccionar idiomas de destino**
```yaml
enabled_languages:
  - en    # English (always enabled)
  - zh    # Chinese
  - ja    # Japanese
  - ko    # Korean
  # - es  # Spanish - comment out languages you don't need
  # - fr  # French
  # - ru  # Russian
```

#### **Agregar términos específicos del proyecto**
```yaml
protected_terms:
  # Add your project terms at the end of the list
  - "YourProjectName"
  - "YourSpecialFeature"
  - "YourAPI"
```

#### **Configuración del modo de sobrescritura**
```yaml
translation:
  overwrite_mode: "auto"  # Smart overwrite mode
  # Options: "always", "never", "auto", "create_new"
```

### **4.2 Explicación de la configuración**
- **`enabled`**: Controla si se habilita la traducción automática
- **`mode`**: Modo de traducción: `"free"` (sin la clave API) o `"api"` (mayor calidad)
- **`enabled_languages`**: Lista de idiomas de destino a los que se traducirá
- **`protected_terms`**: Lista de términos que no deben traducirse
- **`output_dir`**: Directorio de salida para los archivos de traducción (predeterminado: `locales`)
- **`overwrite_mode`**: Modo de sobrescritura
- `"always"`: Sobrescribir siempre las traducciones existentes
- `"never"`: No sobrescribir nunca las traducciones existentes
- `"auto"`: Sobrescritura inteligente (recomendado)
- `"create_new"`: Crear nuevos archivos con sufijo de fecha

### **4.3 Comparación de modos**

| Característica | Modo gratuito | Modo API |
|---------|-----------|----------|
| **Clave API** | ❌ No se necesita | ✅ Se requiere |
| **Costo** | 🆓 Completamente gratis | 💰 Pago por uso |
| **Calidad de la traducción** | ⭐⭐⭐⭐ Buena | ⭐⭐⭐⭐⭐ Excelente |
| **Estabilidad** | ⭐⭐⭐ Moderada | ⭐⭐⭐⭐⭐ Muy estable |
| **Dificultad de configuración** | ⭐⭐⭐⭐⭐ Sin configuración | ⭐⭐ Requiere configuración de API |

---

## 🧪 **Paso 5: Probar el sistema de traducción**

### **5.1 Archivos de confirmación**
```bash
git add .github/
git commit -m "Add auto-translation system"
git push origin main
```

### **5.2 Prueba de activación manual**

**Para el modo gratuito:**
1. En el repositorio GitHub, haz clic en la pestaña **"Acciones"**
2. Selecciona el flujo de trabajo **"Autotraducir README (Gratis)"**
3. Haz clic en el botón **"Ejecutar flujo de trabajo"**
4. Selecciona la rama `main`
5. Haz clic en el botón verde **"Ejecutar flujo de trabajo"**

**Para el modo API:**
1. Seleccione el flujo de trabajo **"Traducir automáticamente README (API)"**
2. Siga los mismos pasos anteriores

### **5.3 Supervisión de la ejecución**
1. Haga clic en la instancia del flujo de trabajo en ejecución.
2. Haga clic en el trabajo `translate`.
3. Expanda cada paso para ver los registros de ejecución.
4. Compruebe si hay mensajes de error.

### **5.4 Verificar resultados**
Tras una ejecución exitosa, debería ver los archivos recién generados en su repositorio:
```
locales/
├── README_en.md    # English version (for completeness)
├── README_zh.md    # Chinese version
├── README_ja.md    # Japanese version
└── README_ko.md    # Korean version (if enabled)
```

**Nota**: La carpeta `locales/` se crea automáticamente durante la primera traducción.

---

## 🔄 **Paso 6: Flujo de trabajo automatizado**

### **6.1 Activación automática**
El sistema ejecutará automáticamente la traducción en las siguientes situaciones:
- Al actualizar el archivo `README.md` y enviarlo a la rama `main`
- Solo se retraduce cuando el archivo de origen es más reciente que los archivos de traducción (traducción incremental)

### **6.2 Resultados de la traducción**
Cada archivo de traducción contiene:
- 🌍 **Elegante tabla de navegación por idioma** - Con iconos de banderas para cambiar de idioma fácilmente
- 📝 **Contenido traducido** - Mantiene el formato y los bloques de código originales
- 🔗 **Información de pie de página localizada** - Contiene notas de traducción y enlaces al proyecto
- 🛡️ **Protección manual contra edición** - Detecta y protege automáticamente las modificaciones del usuario

---

## 💡 **Consejos de uso**

### **🎛️ Control de traducción**

#### **Control completo de detención vs sobrescritura**

Hay dos formas diferentes de controlar el sistema de traducción:

**1. Detener la traducción automática por completo:**
```yaml
translation:
  enabled: false                     # Stops all translation activity
```
- ✅ Las acciones GitHub se ejecutarán, pero finalizarán inmediatamente.
- ✅ No se realizarán llamadas API (ahorra costes para el modo API).
- ✅ No se crearán ni actualizarán archivos.

**2. Controlar la sobrescritura de archivos:**
```yaml
translation:
  overwrite_mode: "never"            # Controls file overwrite behavior
```
- ✅ GitHub Las acciones se seguirán ejecutando
- ✅ Se crearán nuevos archivos de traducción si no existen
- ❌ NO se actualizarán los archivos de traducción existentes

**3. Forzar traducción (activación manual):**
Ambos flujos de trabajo admiten la opción `force_translate` cuando se activan manualmente:
- Configúrelo en `true` para anular la configuración `enabled: false`
- Útil para traducciones puntuales sin modificar la configuración

#### **Comparación del modo de sobrescritura**

| Modo | Disparo automático | Sobrescribir existente | Crear nuevos archivos |
|------|--------------|-------------------|------------------|
| `enabled: false` | ❌ El script sale | ❌ | ❌ |
| `overwrite_mode: "never"` | ✅ Se ejecuta | ❌ Omitir existente | ✅ Crea nuevo |
| `overwrite_mode: "auto"` | ✅ Se ejecuta | 🤔 Detección inteligente | ✅ Crea nuevo |
| `overwrite_mode: "always"` | ✅ Se ejecuta | ✅ Siempre sobrescribe | ✅ Crea nuevo |

### **Ahorra API Costos (Modo API)**
1. **Usar modo gratuito**: Configura `mode: "free"` para costo cero
2. **Desactivar traducción**: Configura `enabled: false` en `i18n-config.yml`
3. **Reducir idiomas**: Activa solo los idiomas que realmente necesitas
4. **Traducción incremental**: El sistema traduce automáticamente solo el contenido actualizado

### **Protección de plazos personalizada**
Añadir a `protected_terms`:
- Nombres de proyectos
- Nombres de funciones especiales
- Nombres de puntos finales API
- Nombres de marcas

### **Proteger ediciones manuales**
Añadir marcadores en los archivos de traducción para proteger las modificaciones manuales:
```markdown
<!-- MANUAL EDIT -->
This content will not be overwritten by auto-translation
```

### **Supervisar la calidad de la traducción**
- **Modo gratuito**: Ideal para la mayoría de los casos de uso, completamente gratis
- **Modo API**: Mayor precisión para proyectos profesionales
- Verificar periódicamente los resultados de la traducción
- Ajustar los términos protegidos según sea necesario
- Corregir manualmente los archivos de traducción cuando sea necesario

---

## 🛠️ **Solución de problemas**

### **Problemas comunes**

#### **Error de clave API**
```
Error: API connection failed: 403 Forbidden
```
**Solución**: Compruebe si la clave API está configurada correctamente y tiene permisos suficientes

#### **Traducción omitida**
```
Skipping zh: locales/README_zh.md is up to date
```
**Explicación**: Este es un comportamiento normal de traducción incremental; el archivo fuente no se ha actualizado.

#### **Traducción deshabilitada**
```
Translation is disabled in configuration
```
**Solución**: Establezca `enabled: true` en `i18n-config.yml` o use el disparador manual con `force_translate: true`

#### **Flujo de trabajo incorrecto seleccionado**
**Problema**: Usar el flujo de trabajo API sin la clave API o viceversa
**Solución**:
- Para el modo gratuito: Usar el flujo de trabajo "Traducir automáticamente README (Gratuito)"
- Para el modo API: Usar el flujo de trabajo "Traducir automáticamente README (API)" y asegurarse de que la clave API esté configurada

### **Obtener ayuda**
- Ver [project documentation](https://github.com/1038lab/i18n)
- Enviar un [Issue](https://github.com/1038lab/i18n/issues)
- Consultar los registros de ejecución de acciones

---

## 🎉 **¡Completo!**

¡Tu proyecto ahora cuenta con traducción automática! Cada vez que actualices README.md, el sistema generará automáticamente versiones multilingües, lo que hará tu proyecto más accesible para usuarios de todo el mundo.

---

> 🌐 Esta guía es proporcionada por el proyecto [i18n](https://github.com/1038lab/i18n)


---
> 🌐 Este documento fue traducido automáticamente con Google Translate. Consulte la [versión en inglés](./README_en.md) para mayor precisión | Herramienta: [i18n](https://github.com/1038lab/i18n)

<!-- AUTO-GENERATED TRANSLATION - To prevent overwriting, add "MANUAL EDIT" comment anywhere in this file -->