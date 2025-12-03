$(function () {
  let selectedImg = null;

  $(".source-img")
    .click(function () {
      $(".source-img").css("border-color", "#ccc");
      $(this).css("border-color", "blue");
      selectedImg = $(this);
      $("#status").text("Выбрана: " + $(this).attr("alt"));
    })
    .first()
    .click();

  $("#add").click(function () {
    if (!selectedImg) return alert("Выберите картинку!");

    const targets = [];
    $('input[name="target"]:checked').each(function () {
      targets.push($(this).val());
    });

    if (targets.length === 0) return alert("Выберите абзацы!");

    const mode = $('input[name="mode"]:checked').val();
    const pos = $('input[name="pos"]:checked').val();

    const $copy = selectedImg
      .clone()
      .removeClass("source-img")
      .addClass("added-img")
      .css({
        display: "block",
        margin: "10px 0",
        "max-width": "200px",
        height: "auto",
        border: "1px solid #666",
      });

    targets.forEach((id) => {
      if (pos === "prepend") {
        $copy.clone().prependTo("#" + id);
      } else {
        $copy.clone().appendTo("#" + id);
      }
    });

    if (mode === "move") {
      selectedImg.remove();
      selectedImg = $(".source-img").first();
      if (selectedImg.length) selectedImg.click();
    }

    $("#status").text(`Картинка добавлена в ${targets.length} абзац(ев)`);
  });

  $("#clear").click(function () {
    $(".added-img").remove();
    $("#status").text("Все добавленные картинки удалены");
  });
});
