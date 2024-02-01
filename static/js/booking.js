"use strict";

$(async function () {
  $("#book").on("click", book);
  $("#cancel").on("click", cancel);

  const urlParams = new URLSearchParams({ listingId })
  console.log("urlParams:", urlParams)
  const response = await fetch(`/api/bookings/${urlParams}`);
  const result = response.data;
  console.log("1st response:", response.data);

  if ("error" in result) {
    console.log(result.error);
  } else {
    let bookings = result.bookings;
    if (bookings) $("#cancel").show();
    else $("#book").show();
  }
});

async function book(evt) {
  evt.preventDefault();

  let response = await fetch("/api/book",
    {
      method:"POST",
      body:JSON.stringify({ listing_id: listingId })
    });

  let result = response.data;

  if ("error" in result) {
    console.log(result.error);
  } else {
    $("#book").hide();
    $("#cancel").show();
  }
}

async function cancel(evt) {
  evt.preventDefault();

  let response = await fetch("/api/cancel",
  {
    method:"POST",
    body:JSON.stringify({ listing_id: listingId })
  });
  let result = response.data;

  if ("error" in result) {
    console.log(result.error);
  } else {
    $("#cancel").hide();
    $("#book").show();
  }
}