@set LocalPath="C:\Users\daniel\Google Drive\Projects\Kolabori\Blink Documentos\trend-layout-2\blink-app\"

@if not exist initialSet (
	@mkdir static\css
	@mkdir static\js
	@mkdir static\mov
	@rename static\images img

	@echo > initialSet
)


@xcopy /Y %LocalPath%templates\*.* templates
@xcopy /Y %LocalPath%css\*.* static\css
@xcopy /Y %LocalPath%js\*.* static\js
@xcopy /Y %LocalPath%mov\*.* static\mov

@xcopy /Y %LocalPath%img\*.* static\img


